<?php
/**
 * Página não encontrada no layout novo.
 */

crom_header();
crom_phead( 'Página não encontrada', 'O endereço pode ter mudado. Veja os serviços abaixo ou fale com a gente.' );
?>
<div class="band"><div class="wrap">
	<div class="btns">
		<a class="btn btn-ink" href="<?php echo crom_url( '/servicos/' ); ?>">Ver serviços</a>
		<a class="btn btn-ink" href="<?php echo crom_url( '/blog/' ); ?>">Ir para o blog</a>
		<a class="btn btn-y" href="<?php echo crom_url( '/contato/' ); ?>">Falar com a CROM</a>
	</div>
</div></div>
<?php
crom_footer();
