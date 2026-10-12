<?php
/**
 * Blog, categorias e busca no layout novo.
 */

crom_header();

if ( is_category() ) {
	$titulo = single_cat_title( '', false );
	$lead   = wp_strip_all_tags( category_description() ) ?: 'Artigos técnicos da CROM Engenharia sobre ' . strtolower( $titulo ) . '.';
	$crumbs = array( array( 'Blog', home_url( '/blog/' ) ), $titulo );
} elseif ( is_search() ) {
	$titulo = 'Busca: ' . get_search_query();
	$lead   = '';
	$crumbs = array( array( 'Blog', home_url( '/blog/' ) ), 'Busca' );
} else {
	$titulo = 'Blog técnico';
	$lead   = 'Preços, normas, projetos e dicas práticas sobre estruturas metálicas, containers, linha de vida e máquinas.';
	$crumbs = array( 'Blog' );
}
crom_phead( $titulo, $lead, $crumbs );

$atual = is_category() ? get_queried_object_id() : 0;
$cats  = get_categories( array( 'hide_empty' => true, 'exclude' => array( get_option( 'default_category' ) ) ) );
?>
<div class="band"><div class="wrap blog-layout">
	<div>
		<nav class="chips" aria-label="Categorias">
			<a class="chip" href="<?php echo crom_url( '/blog/' ); ?>"<?php echo $atual ? '' : ' aria-current="page"'; ?>>Todos</a>
			<?php foreach ( $cats as $c ) : ?>
				<a class="chip" href="<?php echo esc_url( get_category_link( $c ) ); ?>"<?php echo $atual === $c->term_id ? ' aria-current="page"' : ''; ?>><?php echo esc_html( $c->name ); ?></a>
			<?php endforeach; ?>
		</nav>
		<?php if ( have_posts() ) : ?>
			<?php
			while ( have_posts() ) :
				the_post();
				$c = get_the_category();
				?>
				<a class="post-row" href="<?php the_permalink(); ?>">
					<div class="ph"><?php the_post_thumbnail( 'medium_large', array( 'loading' => 'lazy', 'alt' => '' ) ); ?></div>
					<div class="tx">
						<span class="eyebrow"><?php echo $c ? esc_html( $c[0]->name ) . ' · ' : ''; ?><?php echo esc_html( get_the_date( 'j M Y' ) ); ?> · <?php echo (int) crom_minutos(); ?> min de leitura</span>
						<h2 class="h3"><?php the_title(); ?></h2>
						<p><?php echo esc_html( wp_trim_words( get_the_excerpt(), 26 ) ); ?></p>
					</div>
				</a>
			<?php endwhile; ?>
			<div class="pager"><?php the_posts_pagination( array( 'mid_size' => 1, 'prev_text' => '← Anteriores', 'next_text' => 'Próximos →' ) ); ?></div>
		<?php else : ?>
			<p>Nenhum artigo encontrado.</p>
		<?php endif; ?>
	</div>
	<aside class="aside">
		<div class="box"><p class="eyebrow">Orçamento</p><h2 class="h3">Precisa de uma solução para sua obra?</h2><a class="btn btn-y" href="<?php echo crom_url( '/contato/' ); ?>#orcamento">Falar com um engenheiro</a></div>
		<div class="box-light"><p class="eyebrow">Serviços</p>
			<a href="<?php echo crom_url( '/estruturas-metalicas/' ); ?>">Estruturas Metálicas</a>
			<a href="<?php echo crom_url( '/containers-metalicos/' ); ?>">Containers Metálicos</a>
			<a href="<?php echo crom_url( '/linha-de-vida/' ); ?>">Linha de Vida NR-35</a>
			<a href="<?php echo crom_url( '/laudos-tecnicos-maquinas/' ); ?>">Laudos de Máquinas</a>
		</div>
	</aside>
</div></div>
<?php
crom_footer();
