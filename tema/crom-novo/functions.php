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

define( 'CROM_VER', '1.0.4' );
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

/* Arquivos: no layout novo carrega só o CSS/JS do tema e remove o que Elementor, Astra e addons colocam na página. */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! crom_usa_layout() ) {
		return;
	}
	wp_enqueue_style( 'crom', get_stylesheet_directory_uri() . '/assets/crom.css', array(), CROM_VER );
	wp_enqueue_script( 'crom', get_stylesheet_directory_uri() . '/assets/crom.js', array(), CROM_VER, array( 'in_footer' => true, 'strategy' => 'defer' ) );
}, 999 );

function crom_limpa_arquivos() {
	if ( ! crom_usa_layout() ) {
		return;
	}
	global $wp_styles, $wp_scripts;
	$css_ok = array( 'crom', 'wp-block-library', 'global-styles', 'classic-theme-styles', 'core-block-supports', 'wp-img-auto-sizes-contain' );
	$js_ok  = array( 'crom' );
	foreach ( (array) $wp_styles->queue as $h ) {
		if ( ! in_array( $h, $css_ok, true ) ) {
			wp_dequeue_style( $h );
		}
	}
	foreach ( (array) $wp_scripts->queue as $h ) {
		if ( ! in_array( $h, $js_ok, true ) ) {
			wp_dequeue_script( $h );
		}
	}
}
add_action( 'wp_print_styles', 'crom_limpa_arquivos', 9999 );
add_action( 'wp_print_scripts', 'crom_limpa_arquivos', 9999 );
add_action( 'wp_footer', 'crom_limpa_arquivos', 19 );
add_action( 'wp_print_footer_scripts', 'crom_limpa_arquivos', 1 );

/* Pré-carrega as duas fontes que aparecem primeiro na tela. */
add_action( 'wp_head', function () {
	if ( ! crom_usa_layout() ) {
		return;
	}
	$u = get_stylesheet_directory_uri() . '/assets/fonts/';
	foreach ( array( 'IBMPlexSans-400-latin.woff2', 'BarlowCondensed-700-latin.woff2' ) as $f ) {
		echo '<link rel="preload" href="' . esc_url( $u . $f ) . '" as="font" type="font/woff2" crossorigin>' . "\n";
	}
}, 2 );

/* Remove os emojis do WordPress (script e CSS desnecessários). */
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );

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

/* ---------- Google Analytics 4 e medição de contatos ---------- */

/* ID do GA4 (G-XXXXXXX), editável pela API REST em /wp/v2/settings. */
add_action( 'init', function () {
	register_setting( 'general', 'crom_ga4_id', array(
		'type'              => 'string',
		'default'           => '',
		'show_in_rest'      => true,
		'sanitize_callback' => function ( $v ) {
			$v = strtoupper( trim( (string) $v ) );
			return preg_match( '/^G-[A-Z0-9]{4,20}$/', $v ) ? $v : '';
		},
		'description'       => 'ID de medição do Google Analytics 4.',
	) );
} );

/* Código do GA4. Não mede quem está logado editando o site. */
add_action( 'wp_head', function () {
	$id = get_option( 'crom_ga4_id' );
	if ( ! $id || ( is_user_logged_in() && current_user_can( 'edit_posts' ) ) ) {
		return;
	}
	?>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr( $id ); ?>"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','<?php echo esc_js( $id ); ?>');</script>
	<?php
}, 1 );
