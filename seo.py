import os
from urllib.parse import urljoin

from flask import Response, render_template, request
from flask_login import current_user


SITE_NAME = "FlashMatty"

SITE_DESCRIPTION = (
    "Aprenda matemática com exercícios progressivos, desafios, "
    "conquistas, moedas, perfis personalizados e partidas "
    "multiplayer no FlashMatty."
)


def _site_url():
    valor = str(os.getenv("SITE_URL", "") or "").strip()
    if valor:
        return valor.rstrip("/")
    return request.url_root.rstrip("/")


def registrar_seo(app):
    if app.extensions.get("flashmatty_seo_registrado"):
        return

    app.extensions["flashmatty_seo_registrado"] = True

    @app.context_processor
    def contexto_seo():
        site_url = _site_url()
        caminho = request.path or "/"
        canonical = site_url + ("/" if caminho == "/" else caminho)

        return {
            "seo_site_name": SITE_NAME,
            "seo_site_url": site_url,
            "seo_default_description": SITE_DESCRIPTION,
            "seo_canonical_default": canonical,
            "seo_og_image_default": (
                site_url
                + "/static/img/seo/flashmatty-og.png"
            ),
            "seo_google_verification": os.getenv(
                "GOOGLE_SITE_VERIFICATION",
                ""
            ).strip(),
        }

    @app.before_request
    def pagina_publica_inicial():
        if request.method != "GET":
            return None

        if request.path != "/":
            return None

        if current_user.is_authenticated:
            return None

        site_url = _site_url()

        return render_template(
            "index_publico.html",
            seo_index=True,
            seo_title=(
                "FlashMatty - Aprenda Matemática Jogando"
            ),
            seo_description=SITE_DESCRIPTION,
            seo_canonical=site_url + "/",
            seo_og_image=(
                site_url
                + "/static/img/seo/flashmatty-og.png"
            ),
        )

    def sitemap():
        home = _site_url() + "/"

        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset '
            'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            '  <url>\n'
            f'    <loc>{home}</loc>\n'
            '  </url>\n'
            '</urlset>\n'
        )

        return Response(
            xml,
            content_type="application/xml; charset=utf-8"
        )

    app.add_url_rule(
        "/sitemap.xml",
        endpoint="seo_sitemap",
        view_func=sitemap,
        methods=["GET"]
    )

    def robots():
        sitemap_url = _site_url() + "/sitemap.xml"

        conteudo = "\n".join([
            "User-agent: *",
            "Allow: /",
            "",
            "# Áreas privadas da aplicação",
            "Disallow: /dashboard",
            "Disallow: /configuracoes",
            "Disallow: /jornada",
            "Disallow: /ano/",
            "Disallow: /tema/",
            "Disallow: /assunto/",
            "Disallow: /etapa/",
            "Disallow: /biblioteca",
            "Disallow: /social/",
            "Disallow: /loja/",
            "Disallow: /multiplayer/",
            "Disallow: /notificacoes/",
            "Disallow: /logout",
            "",
            f"Sitemap: {sitemap_url}",
            "",
        ])

        return Response(
            conteudo,
            content_type="text/plain; charset=utf-8"
        )

    app.add_url_rule(
        "/robots.txt",
        endpoint="seo_robots",
        view_func=robots,
        methods=["GET"]
    )

    @app.after_request
    def cabecalhos_seo(resposta):
        caminho = request.path or "/"

        if caminho == "/":
            resposta.headers["X-Robots-Tag"] = (
                "index, follow, "
                "max-image-preview:large, "
                "max-snippet:-1, "
                "max-video-preview:-1"
            )

        elif caminho in {"/login", "/cadastro"}:
            resposta.headers["X-Robots-Tag"] = (
                "noindex, follow"
            )

        elif resposta.mimetype == "text/html":
            resposta.headers["X-Robots-Tag"] = (
                "noindex, nofollow"
            )

        return resposta
