<?php
/**
 * Template Name: CROM Novo
 * Template Post Type: page
 *
 * Página no layout novo. O conteúdo da página traz as próprias seções.
 */

crom_header();
while ( have_posts() ) {
	the_post();
	the_content();
}
crom_footer();
