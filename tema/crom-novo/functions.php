<?php
/**
 * CROM Novo: tema filho do Astra.
 *
 * O layout novo é usado:
 *  - em páginas com o modelo "CROM Novo" (tpl-crom.php);
 *  - no blog, posts, categorias, busca e 404 quando a opção crom_novo_ativo está ligada
 *    (ou para administradores com ?crom_preview=1, para revisar antes de ligar).
 * Desligando a opção, o site volta ao layout antigo do Astra/Elementor.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'CROM_VER', '1.0.0' );
define( 'CROM_WHATS', '5584991519641' );
define( 'CROM_EMAIL', 'comercial@cromengenharia.com' );

require_once __DIR__ . '/inc/partials.php';
require_once __DIR__ . '/inc/orcamento.php';

/* Opção que liga o layout novo no blog/posts (editável pela API REST em /wp/v2/settings). */
add_action( 'init', function () {
	register_setting( 'general', 'crom_novo_ativo', array(
		'type'         => 'boolean',
		'default'      => false,
		'show_in_rest' => true,
		'description'  => 'Liga o layout novo da CROM no blog e nos posts.',
	) );
} );

/* Modo de revisão para administradores: ?crom_preview=1 liga, ?crom_preview=0 desliga. */
add_action( 'init', function () {
	if ( isset( $_GET['crom_preview'] ) && is_user_logged_in() && current_user_can( 'edit_pages' ) ) {
		$on = '1' === $_GET['crom_preview'];
		setcookie( 'crom_preview', $on ? '1' : '', $on ? time() + DAY_IN_SECONDS : time() - 3600, COOKIEPATH, COOKIE_DOMAIN, is_ssl(), true );
		$_COOKIE['crom_preview'] = $on ? '1' : '';
	}
} );

function crom_ativo() {
	if ( get_option( 'crom_novo_ativo' ) ) {
		return true;
	}
	return is_user_logged_in() && current_user_can( 'edit_pages' ) && ! empty( $_COOKIE['crom_preview'] );
}

function crom_usa_layout() {
	if ( is_page_template( 'tpl-crom.php' ) ) {
		return true;
	}
	if ( ! crom_ativo() ) {
		return false;
	}
	return is_singular( 'post' ) || is_home() || is_archive() || is_search() || is_404();
}

add_filter( 'template_include', function ( $template ) {
	if ( is_page_template( 'tpl-crom.php' ) || ! crom_ativo() ) {
		return $template;
	}
	if ( is_singular( 'post' ) ) {
		return __DIR__ . '/single-crom.php';
	}
	if ( is_home() || is_archive() || is_search() ) {
		return __DIR__ . '/archive-crom.php';
	}
	if ( is_404() ) {
		return __DIR__ . '/404-crom.php';
	}
	return $template;
}, 99 );

/* Estilos: no layout novo carrega só o necessário e remove Elementor/Astra/addons. */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! crom_usa_layout() ) {
		return;
	}
	global $wp_styles, $wp_scripts;
	$fora = '/^(elementor|e-|premium|pa-|bdt|prime-slider|astra|swiper|font-awesome|fa-|eael|google-fonts-|ht_ctc|ht-ctc|wp-block-library-theme)/';
	foreach ( (array) $wp_styles->queue as $h ) {
		if ( preg_match( $fora, $h ) ) {
			wp_dequeue_style( $h );
		}
	}
	foreach ( (array) $wp_scripts->queue as $h ) {
		if ( preg_match( $fora, $h ) ) {
			wp_dequeue_script( $h );
		}
	}
	wp_enqueue_style( 'crom-fonts', 'https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap', array(), null );
	wp_enqueue_style( 'crom', get_stylesheet_directory_uri() . '/assets/crom.css', array(), CROM_VER );
	wp_enqueue_script( 'crom', get_stylesheet_directory_uri() . '/assets/crom.js', array(), CROM_VER, true );
}, 999 );

add_filter( 'wp_resource_hints', function ( $urls, $rel ) {
	if ( 'preconnect' === $rel && crom_usa_layout() ) {
		$urls[] = array( 'href' => 'https://fonts.gstatic.com', 'crossorigin' );
	}
	return $urls;
}, 10, 2 );

/* Tempo de leitura em minutos. */
function crom_minutos( $post_id = null ) {
	$t = wp_strip_all_tags( get_post_field( 'post_content', $post_id ?: get_the_ID() ) );
	return max( 1, (int) round( str_word_count( $t ) / 200 ) );
}

/* Serviço relacionado a cada categoria do blog. */
function crom_servico_da_categoria( $post_id = null ) {
	$mapa = array(
		'container'   => array( 'containers-metalicos', 'Fabricação de containers metálicos sob medida' ),
		'linha'       => array( 'linha-de-vida', 'Projeto, instalação e recertificação de linha de vida com ART' ),
		'maquina'     => array( 'laudos-tecnicos-maquinas', 'Laudos técnicos de máquinas pesadas com ART' ),
		'estrutura'   => array( 'estruturas-metalicas', 'Projeto, fabricação e montagem de estruturas metálicas' ),
	);
	foreach ( (array) get_the_category( $post_id ) as $c ) {
		$s = remove_accents( strtolower( $c->name ) );
		foreach ( $mapa as $k => $v ) {
			if ( false !== strpos( $s, $k ) ) {
				return $v;
			}
		}
	}
	return $mapa['estrutura'];
}
