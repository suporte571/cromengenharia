<?php
/**
 * Cabeçalho e rodapé do layout novo.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function crom_url( $path ) {
	return esc_url( home_url( $path ) );
}

function crom_atual( $path ) {
	$req  = trailingslashit( strtok( $_SERVER['REQUEST_URI'] ?? '/', '?' ) );
	$path = trailingslashit( $path );
	if ( '/' === $path ) {
		return '/' === $req ? ' aria-current="page"' : '';
	}
	if ( '/blog/' === $path && ( is_singular( 'post' ) || is_category() ) ) {
		return ' aria-current="page"';
	}
	return 0 === strpos( $req, $path ) ? ' aria-current="page"' : '';
}

function crom_header() {
	$logo = get_stylesheet_directory_uri() . '/assets/logo.png';
	?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class( 'crom' ); ?>>
<?php wp_body_open(); ?>
<a class="skip" href="#conteudo">Ir para o conteúdo</a>
<div class="topbar"><div class="wrap">
	<span>Fábrica: <b>BR-304, Km 507 · Parnamirim/RN</b></span>
	<span>WhatsApp <b>(84) 99151-9641</b><span class="mail"> · <b><?php echo esc_html( CROM_EMAIL ); ?></b></span></span>
</div></div>
<header class="site"><div class="wrap">
	<a class="logo" href="<?php echo crom_url( '/' ); ?>" aria-label="CROM Engenharia, início"><img src="<?php echo esc_url( $logo ); ?>" alt="CROM Engenharia" width="165" height="44"></a>
	<button class="menu-toggle" id="menuToggle" aria-expanded="false" aria-controls="mainNav">Menu</button>
	<nav class="main" id="mainNav" aria-label="Menu principal">
		<a href="<?php echo crom_url( '/' ); ?>"<?php echo crom_atual( '/' ); ?>>Início</a>
		<a href="<?php echo crom_url( '/quem-somos/' ); ?>"<?php echo crom_atual( '/quem-somos/' ); ?>>Quem Somos</a>
		<div class="has-sub">
			<a href="<?php echo crom_url( '/servicos/' ); ?>"<?php echo crom_atual( '/servicos/' ); ?>>Serviços <span aria-hidden="true">▾</span></a>
			<div class="sub">
				<a href="<?php echo crom_url( '/estruturas-metalicas/' ); ?>">Estruturas Metálicas<small>galpões · coberturas · mezaninos</small></a>
				<a href="<?php echo crom_url( '/containers-metalicos/' ); ?>">Containers Metálicos<small>fabricação sob medida</small></a>
				<a href="<?php echo crom_url( '/linha-de-vida/' ); ?>">Linha de Vida<small>NR-35 · projeto e laudo</small></a>
				<a href="<?php echo crom_url( '/laudos-tecnicos-maquinas/' ); ?>">Laudos de Máquinas<small>NR-12 · munck · escavadeiras</small></a>
			</div>
		</div>
		<a href="<?php echo crom_url( '/obras/' ); ?>"<?php echo crom_atual( '/obras/' ); ?>>Obras</a>
		<a href="<?php echo crom_url( '/blog/' ); ?>"<?php echo crom_atual( '/blog/' ); ?>>Blog</a>
		<a href="<?php echo crom_url( '/contato/' ); ?>"<?php echo crom_atual( '/contato/' ); ?>>Contato</a>
		<a class="btn btn-y" href="<?php echo crom_url( '/contato/' ); ?>#orcamento">Solicitar orçamento</a>
	</nav>
</div></header>
<main id="conteudo">
	<?php
}

function crom_footer() {
	$logo = get_stylesheet_directory_uri() . '/assets/logo-branco.png';
	?>
</main>
<div class="stripe" aria-hidden="true"></div>
<footer class="site"><div class="wrap">
	<div class="cols">
		<div><img class="flogo" src="<?php echo esc_url( $logo ); ?>" alt="CROM Engenharia" width="150" height="40" loading="lazy"><p>Projeto, fabricação e montagem de estruturas metálicas, containers metálicos, linha de vida e laudos técnicos.</p></div>
		<div><h2 class="fh">Serviços</h2><ul>
			<li><a href="<?php echo crom_url( '/estruturas-metalicas/' ); ?>">Estruturas Metálicas</a></li>
			<li><a href="<?php echo crom_url( '/containers-metalicos/' ); ?>">Containers Metálicos</a></li>
			<li><a href="<?php echo crom_url( '/linha-de-vida/' ); ?>">Linha de Vida</a></li>
			<li><a href="<?php echo crom_url( '/laudos-tecnicos-maquinas/' ); ?>">Laudos de Máquinas</a></li>
		</ul></div>
		<div><h2 class="fh">Empresa</h2><ul>
			<li><a href="<?php echo crom_url( '/quem-somos/' ); ?>">Quem Somos</a></li>
			<li><a href="<?php echo crom_url( '/obras/' ); ?>">Obras</a></li>
			<li><a href="<?php echo crom_url( '/blog/' ); ?>">Blog</a></li>
			<li><a href="<?php echo crom_url( '/contato/' ); ?>">Contato</a></li>
		</ul></div>
		<div><h2 class="fh">Contato</h2><ul>
			<li><a href="https://wa.me/<?php echo CROM_WHATS; ?>" target="_blank" rel="noopener">WhatsApp (84) 99151-9641</a></li>
			<li>(84) 99650-7337 · (84) 99106-0289</li>
			<li><a href="mailto:<?php echo esc_attr( CROM_EMAIL ); ?>"><?php echo esc_html( CROM_EMAIL ); ?></a></li>
			<li>BR-304, Km 507, s/n · Encanto Verde<br>Parnamirim/RN · 59146-750</li>
		</ul></div>
	</div>
	<div class="legal"><span>© <?php echo esc_html( gmdate( 'Y' ) ); ?> CROM Engenharia · CNPJ 34.629.759/0001-50</span><span>CREA-RN 200005964-2</span></div>
</div></footer>
<a class="wa" href="https://wa.me/<?php echo CROM_WHATS; ?>?text=<?php echo rawurlencode( 'Olá! Vim pelo site e gostaria de um orçamento.' ); ?>" target="_blank" rel="noopener" aria-label="Falar no WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg><span>WhatsApp</span></a>
<?php wp_footer(); ?>
</body>
</html>
	<?php
}

/* Cabeçalho escuro das páginas internas. */
function crom_phead( $titulo, $lead = '', $crumbs = array(), $bg = '' ) {
	echo '<div class="phead">';
	if ( $bg ) {
		echo '<img class="bg" src="' . esc_url( $bg ) . '" alt="">';
	}
	echo '<div class="wrap">';
	if ( $crumbs ) {
		$p = array( '<a href="' . crom_url( '/' ) . '">Início</a>' );
		foreach ( $crumbs as $c ) {
			$p[] = is_array( $c ) ? '<a href="' . esc_url( $c[1] ) . '">' . esc_html( $c[0] ) . '</a>' : esc_html( $c );
		}
		echo '<p class="crumbs">' . implode( ' / ', $p ) . '</p>';
	}
	echo '<h1>' . esc_html( $titulo ) . '</h1>';
	if ( $lead ) {
		echo '<p class="lead">' . wp_kses_post( $lead ) . '</p>';
	}
	echo '</div></div>';
}
