<?php
/**
 * Post do blog no layout novo.
 */

crom_header();
while ( have_posts() ) :
	the_post();
	$cats = get_the_category();
	$cat  = $cats ? $cats[0] : null;
	$serv = crom_servico_da_categoria();
	?>
	<article>
		<div class="phead"><div class="wrap">
			<p class="crumbs"><a href="<?php echo crom_url( '/' ); ?>">Início</a> / <a href="<?php echo crom_url( '/blog/' ); ?>">Blog</a><?php if ( $cat ) : ?> / <a href="<?php echo esc_url( get_category_link( $cat ) ); ?>"><?php echo esc_html( $cat->name ); ?></a><?php endif; ?></p>
			<h1 class="post-title"><?php the_title(); ?></h1>
			<div class="post-meta">
				<?php if ( $cat ) : ?><span><?php echo esc_html( $cat->name ); ?></span><?php endif; ?>
				<span><time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( get_the_date( 'j M Y' ) ); ?></time></span>
				<span><?php echo (int) crom_minutos(); ?> min de leitura</span>
				<span>Equipe de engenharia CROM</span>
			</div>
		</div></div>
		<div class="band"><div class="wrap article">
			<nav class="toc" id="toc" aria-label="Neste artigo"><p class="eyebrow">Neste artigo</p></nav>
			<div class="prose" id="prose">
				<?php
				if ( has_post_thumbnail() ) {
					the_post_thumbnail( 'large', array( 'class' => 'feat', 'fetchpriority' => 'high' ) );
				}
				the_content();
				?>
				<div class="box">
					<p class="eyebrow">Serviço CROM</p>
					<h2 class="h3"><?php echo esc_html( $serv[1] ); ?></h2>
					<p>Fábrica em Parnamirim/RN e atendimento em todo o Brasil.</p>
					<div class="btns"><a class="btn btn-y" href="<?php echo crom_url( '/' . $serv[0] . '/' ); ?>">Conhecer o serviço</a><a class="btn btn-o" href="https://wa.me/<?php echo CROM_WHATS; ?>" target="_blank" rel="noopener">WhatsApp</a></div>
				</div>
				<div class="author"><div class="av"><img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/logo.png' ); ?>" alt=""></div><div><strong>Equipe de engenharia CROM</strong><p class="note">Conteúdo técnico da CROM Engenharia · CREA-RN 200005964-2</p></div></div>
			</div>
		</div></div>
	</article>
	<?php
endwhile;
crom_footer();
