<?php
/**
 * Formulário de orçamento: shortcode [crom_orcamento].
 * Envia e-mail para comercial@cromengenharia.com e volta para a página com aviso de sucesso.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_shortcode( 'crom_orcamento', function () {
	$ok   = isset( $_GET['enviado'] ) && '1' === $_GET['enviado'];
	$erro = isset( $_GET['enviado'] ) && '0' === $_GET['enviado'];
	ob_start();
	?>
	<form class="quote" id="orcamento" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
		<?php if ( $ok ) : ?>
			<div class="full ok" role="status">Recebemos seu pedido. Um engenheiro da CROM vai responder em horário comercial. Se for urgente, chame no WhatsApp (84) 99151-9641.</div>
		<?php elseif ( $erro ) : ?>
			<div class="full err" role="alert">Não foi possível enviar. Confira nome e WhatsApp, ou fale direto pelo WhatsApp (84) 99151-9641.</div>
		<?php endif; ?>
		<input type="hidden" name="action" value="crom_orcamento">
		<?php wp_nonce_field( 'crom_orcamento', 'crom_nonce' ); ?>
		<label class="hp" aria-hidden="true">Não preencha<input name="site_url" tabindex="-1" autocomplete="off"></label>
		<label>Nome<input id="f-nome" name="nome" autocomplete="name" required></label>
		<label>Empresa<input id="f-empresa" name="empresa" autocomplete="organization"></label>
		<label>WhatsApp<input id="f-tel" name="tel" type="tel" autocomplete="tel" placeholder="(84) 9 0000-0000" required></label>
		<label>E-mail<input id="f-email" name="email" type="email" autocomplete="email"></label>
		<label>Serviço<select id="f-servico" name="servico"><option>Estrutura metálica</option><option>Container metálico</option><option>Linha de vida</option><option>Laudo de máquina</option><option>Outro</option></select></label>
		<label>Cidade / UF<input id="f-cidade" name="cidade" placeholder="Parnamirim/RN"></label>
		<label class="full">Descreva a necessidade<textarea id="f-msg" name="msg" placeholder="Ex.: cobertura metálica de 20 x 30 m para estacionamento"></textarea></label>
		<div class="full"><button class="btn btn-y" type="submit">Enviar pedido de orçamento</button></div>
	</form>
	<?php
	return ob_get_clean();
} );

function crom_orcamento_enviar() {
	$volta = wp_get_referer() ? wp_get_referer() : home_url( '/contato/' );
	$volta = remove_query_arg( 'enviado', $volta );
	$falha = add_query_arg( 'enviado', '0', $volta ) . '#orcamento';

	if ( ! isset( $_POST['crom_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['crom_nonce'] ) ), 'crom_orcamento' ) ) {
		wp_safe_redirect( $falha );
		exit;
	}
	if ( ! empty( $_POST['site_url'] ) ) { // honeypot
		wp_safe_redirect( add_query_arg( 'enviado', '1', $volta ) . '#orcamento' );
		exit;
	}
	$c = array();
	foreach ( array( 'nome', 'empresa', 'tel', 'email', 'servico', 'cidade' ) as $k ) {
		$c[ $k ] = isset( $_POST[ $k ] ) ? sanitize_text_field( wp_unslash( $_POST[ $k ] ) ) : '';
	}
	$msg = isset( $_POST['msg'] ) ? sanitize_textarea_field( wp_unslash( $_POST['msg'] ) ) : '';
	if ( '' === $c['nome'] || '' === $c['tel'] ) {
		wp_safe_redirect( $falha );
		exit;
	}
	$corpo = "Novo pedido de orçamento pelo site\n\n"
		. "Nome: {$c['nome']}\nEmpresa: {$c['empresa']}\nWhatsApp: {$c['tel']}\nE-mail: {$c['email']}\n"
		. "Serviço: {$c['servico']}\nCidade/UF: {$c['cidade']}\n\nMensagem:\n{$msg}\n";
	$headers = array();
	if ( is_email( $c['email'] ) ) {
		$headers[] = 'Reply-To: ' . $c['nome'] . ' <' . $c['email'] . '>';
	}
	$enviado = wp_mail( CROM_EMAIL, 'Orçamento pelo site: ' . $c['servico'] . ' - ' . $c['nome'], $corpo, $headers );
	wp_safe_redirect( add_query_arg( 'enviado', $enviado ? '1' : '0', $volta ) . '#orcamento' );
	exit;
}
add_action( 'admin_post_nopriv_crom_orcamento', 'crom_orcamento_enviar' );
add_action( 'admin_post_crom_orcamento', 'crom_orcamento_enviar' );
