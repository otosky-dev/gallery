@echo off
rem Genere la galerie puis la publie sur Cloudflare Pages.
rem Usage : deploy.cmd   (depuis n importe quel dossier)
cd /d "%~dp0"
rem Repart d un dossier vide : Sigal ne supprime jamais les fichiers
rem renommes ou retires, ils seraient sinon publies a nouveau.
if exist ..\..\gallery_site rmdir /s /q ..\..\gallery_site
.venv\Scripts\sigal build || exit /b 1
npx wrangler pages deploy ..\..\gallery_site --project-name galerie --branch main --commit-dirty=true
