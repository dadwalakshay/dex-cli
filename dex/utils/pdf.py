from PIL import Image

from dex.config import DEFAULT_PDF_NAME


class PDFGenerator:
    def __init__(
        self, filenames: list[str], path: str, post_cleanup: bool = False
    ) -> None:
        self.filenames = filenames
        self.path = path

        self.post_cleanup = post_cleanup

    def generate(self) -> None:
        sorted_filename_iter = filter(
            lambda filename: (".json" not in filename) and (".pdf" not in filename),
            sorted(self.filenames),
        )

        pil_image_ls = list(
            map(
                lambda filename: Image.open(f"{self.path}/{filename}").convert("RGB"),
                sorted_filename_iter,
            )
        )

        if pil_image_ls:
            pil_image_ls[0].save(
                f"{self.path}/{DEFAULT_PDF_NAME}",
                save_all=True,
                append_images=pil_image_ls[1:],
            )

        if self.post_cleanup:
            self.clean_up()

        return

    def clean_up(self) -> None:
        # Still figuring out a safer way to clean-up downloaded and processed files
        # os.system(
        #     f"rm -r {self.path}/*.jpg &&"
        #     f"rm -r {self.path}/*.jpeg &&"
        #     f"rm -r {self.path}/*.png"
        # )

        return
