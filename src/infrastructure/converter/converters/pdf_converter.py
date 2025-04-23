import shutil
import subprocess
from pathlib import Path
from typing import Union

from xhtml2pdf import pisa

from src.infrastructure.converter.base_converter import BaseConverter, ConversionError


class PDFConverter(BaseConverter):
    def convert(
        self, input_source: Union[str, Path], output_target: Union[str, Path]
    ) -> None:
        """
        Convert a file to PDF based on its extension and save to the specified path.

        Determines the conversion method by file extension and delegates to
        the appropriate private helper. Raises ConversionError for unsupported
        formats or conversion failures.

        :param input_source: Path or string pointing to the source file.
        :param output_target: Path or string for the output PDF file.
        :raises ConversionError: if conversion cannot be completed.
        """
        src = Path(input_source)
        dst = Path(output_target)
        ext = src.suffix.lower()

        # Map file extensions to their corresponding converter methods
        converters = {
            ".doc": self._convert_docx,
            ".docx": self._convert_docx,
            ".ppt": self._convert_pptx,
            ".pptx": self._convert_pptx,
            ".html": self._convert_html,
            ".htm": self._convert_html,
            ".xml": self._convert_xml,
        }

        try:
            convert_func = converters[ext]
        except KeyError:
            raise ConversionError(f"Unsupported extension: {ext}")

        convert_func(src, dst)

    def _convert_docx(
        self, src_input: Union[str, Path], dst_input: Union[str, Path]
    ) -> None:
        """
        Convert a DOC(X) file to PDF using LibreOffice.

        :param src_input: Path to the .doc or .docx file.
        :param dst_input: Path where the generated PDF will be saved.
        :raises ConversionError: if conversion fails.
        """
        src = Path(src_input)
        dst = Path(dst_input)
        out_dir = dst.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        self._convert_with_libreoffice(src, out_dir)
        generated = out_dir / f"{src.stem}.pdf"
        if not generated.exists():
            raise ConversionError(f"LibreOffice did not produce {generated}")
        generated.rename(dst)

    def _convert_pptx(
        self, src_input: Union[str, Path], dst_input: Union[str, Path]
    ) -> None:
        """
        Convert a PPT(X) file to PDF, trying native converter first.

        :param src_input: Path to the .ppt or .pptx file.
        :param dst_input: Path where the generated PDF will be saved.
        :raises ConversionError: if conversion fails.
        """
        src = Path(src_input)
        dst = Path(dst_input)
        out_dir = dst.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        try:
            import pptxtopdf  # type: ignore

            pptxtopdf.convert(str(src), str(dst))
            return
        except Exception:
            pass

        self._convert_with_libreoffice(src, out_dir)
        generated = out_dir / f"{src.stem}.pdf"
        if not generated.exists():
            raise ConversionError(f"LibreOffice did not produce {generated}")
        generated.rename(dst)

    def _convert_html(
        self, src_input: Union[str, Path], dst_input: Union[str, Path]
    ) -> None:
        """
        Convert an HTML file to PDF, trying multiple libraries and falling back.

        :param src_input: Path to the .html or .htm file.
        :param dst_input: Path where the generated PDF will be saved.
        :raises ConversionError: if conversion fails.
        """
        src = Path(src_input)
        dst = Path(dst_input)
        out_dir = dst.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1) pyhtml2pdf
        try:
            from pyhtml2pdf import converter  # type: ignore

            converter.convert(str(src), str(dst))
            return
        except Exception:
            pass

        # 2) xhtml2pdf via pisa
        try:
            html_string = src.read_text(encoding="utf-8")
            tmp_pdf = out_dir / f"{src.stem}.pdf"
            with open(tmp_pdf, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)
            if not pisa_status.err and tmp_pdf.exists():
                tmp_pdf.rename(dst)
                return
        except Exception:
            pass

        # 3) Fallback to LibreOffice
        self._convert_with_libreoffice(src, out_dir)
        generated = out_dir / f"{src.stem}.pdf"
        if not generated.exists():
            raise ConversionError(f"LibreOffice did not produce {generated}")
        generated.rename(dst)

    def _convert_xml(
        self, src_input: Union[str, Path], dst_input: Union[str, Path]
    ) -> None:
        """
        Convert an XML file to PDF via multiple strategies:

        1. Wrap raw XML in <pre> and convert using xhtml2pdf (pisa).
        2. If a transform.xsl exists next to this module, apply XSLT to
            produce FO and run Apache FOP.
        3. Fall back to LibreOffice headless conversion.

        :param src_input: Path to the .xml file.
        :param dst_input: Path where the generated PDF will be saved.
        :raises ConversionError: if all methods fail.
        """
        src = Path(src_input)
        dst = Path(dst_input)
        out_dir = dst.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1) xhtml2pdf via pisa
        try:
            xml_content = src.read_text(encoding="utf-8")
            html_wrapped = f"<pre>{xml_content}</pre>"
            with open(dst, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_wrapped, dest=pdf_file)
            if not pisa_status.err and dst.exists():
                return
        except Exception:
            pass

        # 2) XSLT -> FO -> FOP
        try:
            try:
                base_dir = Path(__file__).parent
            except NameError:
                base_dir = Path.cwd()
            transform = base_dir / "transform.xsl"
            if transform.exists():
                from lxml import etree  # type: ignore

                xslt = etree.XSLT(etree.parse(str(transform)))
                fo_tree = xslt(etree.parse(str(src)))
                fo_path = out_dir / f"{src.stem}.fo"
                with open(fo_path, "wb") as f:
                    f.write(etree.tostring(fo_tree))
                subprocess.run(["fop", str(fo_path), str(dst)], check=True)
                if dst.exists():
                    return
        except Exception:
            pass

        # 3) Fall back to LibreOffice
        self._convert_with_libreoffice(src, out_dir)
        generated = out_dir / f"{src.stem}.pdf"
        if not generated.exists():
            raise ConversionError(f"Conversion to PDF failed for XML: {src}")
        generated.rename(dst)

    def _convert_with_libreoffice(self, src: Path, out_dir: Path) -> None:
        """
        Invoke LibreOffice in headless mode to convert a document to PDF.

        Detects the macOS app bundle binary or falls back to the system `soffice` executable.

        :param src: Path to the input document.
        :param out_dir: Directory where LibreOffice will write the PDF.
        :raises RuntimeError: if the `soffice` binary cannot be found.
        """
        bundle = Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
        soffice_bin = str(bundle) if bundle.exists() else shutil.which("soffice") or ""
        if not soffice_bin:
            raise RuntimeError("Could not find 'soffice' executable")

        cmd = [
            soffice_bin,
            "--headless",
            "--convert-to",
            "pdf",
            str(src),
            "--outdir",
            str(out_dir),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
