<?php
/**
 * Formulário de orçamento: shortcode [crom_orcamento].
 * Guarda cada pedido no painel (menu "Pedidos de orçamento"), envia e-mail para
 * comercial@cromengenharia.com e volta para a página com aviso de sucesso.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/* Pedidos ficam guardados no painel, mesmo se o e-mail falhar. */
add_action( 'init', function () {
	register_post_type( 'crom_pedido', array(
		'labels'          => array(
			'name'          => 'Pedidos de orçamento',
			'singular_name' => 'Pedido de orçamento',
			'menu_name'     => 'Pedidos de orçamento',
			'all_items'     => 'Todos os pedidos',
			'edit_item'     => 'Pedido de orçamento',
			'search_items'  => 'Buscar pedidos',
			'not_found'     => 'Nenhum pedido ainda.',
		),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => true,
		'show_in_rest'    => false,
		'menu_position'   => 3,
		'menu_icon'       => 'dashicons-email-alt',
		'capability_type' => 'post',
		'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
		'map_meta_cap'    => true,
		'supports'        => array( 'title', 'editor' ),
	) );
} );

add_filter( 'manage_crom_pedido_posts_columns', function ( $cols ) {
	return array( 'cb' => $cols['cb'], 'title' => 'Cliente', 'crom_tel' => 'WhatsApp', 'crom_serv' => 'Serviço', 'crom_origem' => 'Origem', 'crom_mail' => 'E-mail enviado', 'date' => 'Data' );
} );
add_action( 'manage_crom_pedido_posts_custom_column', function ( $col, $id ) {
	if ( 'crom_tel' === $col ) {
		$t = get_post_meta( $id, '_crom_tel', true );
		$n = ltrim( preg_replace( '/\D/', '', $t ), '0' );
		if ( $n && strlen( $n ) <= 11 ) {
			$n = '55' . $n;
		}
		echo $n ? '<a href="https://wa.me/' . esc_attr( $n ) . '" target="_blank" rel="noopener">' . esc_html( $t ) . '</a>' : '';
	} elseif ( 'crom_serv' === $col ) {
		echo esc_html( get_post_meta( $id, '_crom_servico', true ) );
	} elseif ( 'crom_origem' === $col ) {
		echo esc_html( get_post_meta( $id, '_crom_origem', true ) );
	} elseif ( 'crom_mail' === $col ) {
		echo get_post_meta( $id, '_crom_mail_ok', true ) ? 'Sim' : '<strong style="color:#b32d2e">Não</strong>';
	}
}, 10, 2 );

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
		<input type="hidden" name="origem" id="f-origem" value="">
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
	$origem = isset( $_POST['origem'] ) ? substr( sanitize_text_field( wp_unslash( $_POST['origem'] ) ), 0, 300 ) : '';
	$msg = isset( $_POST['msg'] ) ? sanitize_textarea_field( wp_unslash( $_POST['msg'] ) ) : '';
	if ( '' === $c['nome'] || '' === $c['tel'] ) {
		wp_safe_redirect( $falha );
		exit;
	}
	$corpo = "Novo pedido de orçamento pelo site\n\n"
		. "Nome: {$c['nome']}\nEmpresa: {$c['empresa']}\nWhatsApp: {$c['tel']}\nE-mail: {$c['email']}\n"
		. "Serviço: {$c['servico']}\nCidade/UF: {$c['cidade']}\n\nMensagem:\n{$msg}\n\n"
		. 'Origem do visitante: ' . ( $origem ? $origem : 'não identificada' ) . "\n";
	$pid = wp_insert_post( array(
		'post_type'    => 'crom_pedido',
		'post_status'  => 'private',
		'post_title'   => $c['nome'] . ( $c['empresa'] ? ' (' . $c['empresa'] . ')' : '' ) . ' – ' . $c['servico'],
		'post_content' => $corpo,
	) );
	if ( $pid && ! is_wp_error( $pid ) ) {
		update_post_meta( $pid, '_crom_tel', $c['tel'] );
		update_post_meta( $pid, '_crom_servico', $c['servico'] );
		update_post_meta( $pid, '_crom_origem', $origem );
	}
	$headers = array();
	if ( is_email( $c['email'] ) ) {
		$headers[] = 'Reply-To: ' . $c['nome'] . ' <' . $c['email'] . '>';
	}
	$enviado = wp_mail( CROM_EMAIL, 'Orçamento pelo site: ' . $c['servico'] . ' - ' . $c['nome'], $corpo, $headers );
	if ( $pid && ! is_wp_error( $pid ) ) {
		update_post_meta( $pid, '_crom_mail_ok', $enviado ? 1 : 0 );
	}
	$salvo = ( $pid && ! is_wp_error( $pid ) ) || $enviado;
	wp_safe_redirect( add_query_arg( 'enviado', $salvo ? '1' : '0', $volta ) . '#orcamento' );
	exit;
}
add_action( 'admin_post_nopriv_crom_orcamento', 'crom_orcamento_enviar' );
add_action( 'admin_post_crom_orcamento', 'crom_orcamento_enviar' );
