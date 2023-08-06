from render_engine.hookspec import hook_impl
import pytailwindcss
import pathlib

class TailwindCSS:
    @hook_impl
    def pre_render_build(self, site: "Site"):
        for file in pathlib.Path(site.static_path).glob("**/*.css"):
            pytailwindcss.run(
                auto_install=True,
                tailwindcss_cli_args=[
                    "--input",
                    f"{file.absolute()}",
                    "--output",
                    f"{(site.static_path / file).absolute()}",
                ],
            )