<?php
/**
 * Plugin Name: Oliviks checkout fields
 * Description: Adds an optional doorbell / entry code to checkout and surfaces it on the order screen, in admin order emails, and in the customer confirmation. Also makes the phone number required.
 * Author: BridgeWorks
 * Version: 1.1.0
 *
 * HOW TO USE
 * This is the DEPLOYED copy of the file that lives on the server at
 * /home/olivoilt/public_html/wp-content/mu-plugins/oliviks-checkout-fields.php
 * mu-plugins activate themselves - there is nothing to switch on, and theme or
 * plugin updates cannot remove it. To change wording, edit the label/placeholder
 * strings below and re-upload via cPanel File Manager.
 *
 * To remove the doorbell field entirely: delete the file.
 * To make the phone optional again: delete the two PHP_INT_MAX filters at the end.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'OLIVIKS_DOORBELL_KEY', '_oliviks_doorbell_code' );

add_filter( 'woocommerce_checkout_fields', function ( $fields ) {
	$fields['billing']['oliviks_doorbell_code'] = array(
		'label'       => 'Doorbell / entry code',
		'placeholder' => 'Only if we are delivering to you - e.g. 12B, or ring Kovacs',
		'required'    => false,
		'class'       => array( 'form-row-wide' ),
		'clear'       => true,
		// 73 puts it directly after address_2 (72) in the Hungarian address layout.
		'priority'    => 73,
	);

	if ( isset( $fields['billing']['billing_phone'] ) ) {
		$fields['billing']['billing_phone']['required'] = true;
	}

	return $fields;
}, 20 );

add_action( 'woocommerce_checkout_create_order', function ( $order, $data ) {
	if ( ! empty( $data['oliviks_doorbell_code'] ) ) {
		$order->update_meta_data( OLIVIKS_DOORBELL_KEY, sanitize_text_field( wp_unslash( $data['oliviks_doorbell_code'] ) ) );
	}
}, 10, 2 );

add_action( 'woocommerce_admin_order_data_after_billing_address', function ( $order ) {
	$code = $order->get_meta( OLIVIKS_DOORBELL_KEY );
	if ( $code ) {
		echo '<p><strong>Doorbell / entry code:</strong> ' . esc_html( $code ) . '</p>';
	}
} );

add_filter( 'woocommerce_email_order_meta_fields', function ( $meta_fields, $sent_to_admin, $order ) {
	$code = $order->get_meta( OLIVIKS_DOORBELL_KEY );
	if ( $code ) {
		$meta_fields['oliviks_doorbell_code'] = array(
			'label' => 'Doorbell / entry code',
			'value' => $code,
		);
	}
	return $meta_fields;
}, 10, 3 );

add_filter( 'woocommerce_get_order_item_totals', function ( $rows, $order ) {
	$code = $order->get_meta( OLIVIKS_DOORBELL_KEY );
	if ( $code ) {
		$rows['oliviks_doorbell_code'] = array(
			'label' => 'Doorbell / entry code:',
			'value' => esc_html( $code ),
		);
	}
	return $rows;
}, 10, 2 );

// Something in the theme/plugin stack resets the phone to optional after the
// filters above, so these run last and win.
add_filter( 'woocommerce_default_address_fields', function ( $fields ) {
	if ( isset( $fields['phone'] ) ) {
		$fields['phone']['required'] = true;
	}
	return $fields;
}, PHP_INT_MAX );

add_filter( 'woocommerce_checkout_fields', function ( $fields ) {
	if ( isset( $fields['billing']['billing_phone'] ) ) {
		$fields['billing']['billing_phone']['required'] = true;
	}
	return $fields;
}, PHP_INT_MAX );
