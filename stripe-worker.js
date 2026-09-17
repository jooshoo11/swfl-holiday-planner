/**
 * SWFL Holiday & Festivities Planner - Stripe Connect Split Payments Worker
 * 
 * Free Serverless Backend running on Cloudflare Workers (100,000 free requests/day).
 * Handles:
 *  1. Direct split payments: 90% to homeowner bank, 10% platform fee to creator.
 *  2. Stripe Express Onboarding links for host families.
 * 
 * --------------------------------------------------------------------------
 * 2-MINUTE SETUP INSTRUCTIONS (100% FREE):
 * --------------------------------------------------------------------------
 * 1. Go to https://workers.cloudflare.com and create a free account.
 * 2. Click "Create Application" -> "Create Worker".
 * 3. Delete the default code and paste this entire file.
 * 4. Go to Settings -> Variables -> Environment Variables:
 *      Add Variable: STRIPE_SECRET_KEY = sk_live_... (or sk_test_...)
 * 5. Click "Deploy". Copy your Worker URL (e.g., https://swfl-tips.myworker.workers.dev).
 * 6. Paste your Worker URL in your SWFL Admin Dashboard (Tipping & Payouts tab).
 * --------------------------------------------------------------------------
 */

export default {
  async fetch(request, env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);
    const stripeKey = env.STRIPE_SECRET_KEY || '';

    // Route: Health check
    if (url.pathname === '/' || url.pathname === '/api/health') {
      return new Response(JSON.stringify({
        status: 'active',
        service: 'SWFL Holiday Planner - Stripe Connect Worker',
        configured: Boolean(stripeKey)
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // Route: Create Stripe Checkout Session with 90/10 Split
    if (url.pathname === '/api/create-tip-session' && request.method === 'POST') {
      try {
        if (!stripeKey) {
          throw new Error('STRIPE_SECRET_KEY is not configured in Worker environment variables.');
        }

        const body = await request.json();
        const {
          eventId,
          displayTitle,
          stripeAccountId,
          amountCents,
          platformFeeCents,
          cheerMessage,
          successUrl,
          cancelUrl
        } = body;

        if (!amountCents || amountCents < 100) {
          throw new Error('Invalid tip amount. Minimum is $1.00.');
        }

        // Build Stripe Form Data
        const params = new URLSearchParams();
        params.append('payment_method_types[0]', 'card');
        params.append('mode', 'payment');
        params.append('line_items[0][price_data][currency]', 'usd');
        params.append('line_items[0][price_data][product_data][name]', `Host Tip: ${displayTitle || 'Holiday Light Show'}`);
        params.append('line_items[0][price_data][product_data][description]', '90% directly to host family electric bill & holiday maintenance • 10% platform fee');
        params.append('line_items[0][price_data][unit_amount]', String(amountCents));
        params.append('line_items[0][quantity]', '1');

        params.append('success_url', successUrl || 'https://jooshoo11.github.io/swfl-holiday-planner/?tip_success=true');
        params.append('cancel_url', cancelUrl || 'https://jooshoo11.github.io/swfl-holiday-planner/');

        params.append('metadata[eventId]', eventId || '');
        params.append('metadata[cheerMessage]', cheerMessage || '');

        // If host has onboarded with Stripe Connect, split payment automatically
        if (stripeAccountId && stripeAccountId.startsWith('acct_')) {
          params.append('payment_intent_data[transfer_data][destination]', stripeAccountId);
          params.append('payment_intent_data[application_fee_amount]', String(platformFeeCents || Math.round(amountCents * 0.10)));
        }

        // Call Stripe REST API directly
        const stripeRes = await fetch('https://api.stripe.com/v1/checkout/sessions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${stripeKey}`,
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: params.toString()
        });

        const session = await stripeRes.json();

        if (session.error) {
          throw new Error(session.error.message);
        }

        return new Response(JSON.stringify({ checkoutUrl: session.url, sessionId: session.id }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
    }

    // Route: Create Stripe Connect Express Onboarding Link
    if (url.pathname === '/api/create-onboarding-link') {
      try {
        if (!stripeKey) {
          throw new Error('STRIPE_SECRET_KEY is not configured in Worker.');
        }

        const hostName = url.searchParams.get('host') || 'Host Family';
        const eventId = url.searchParams.get('eventId') || 'event';

        // 1. Create Express Account
        const accParams = new URLSearchParams();
        accParams.append('type', 'express');
        accParams.append('country', 'US');
        accParams.append('capabilities[card_payments][requested]', 'true');
        accParams.append('capabilities[transfers][requested]', 'true');
        accParams.append('business_type', 'individual');
        accParams.append('metadata[eventId]', eventId);
        accParams.append('metadata[hostTitle]', hostName);

        const accRes = await fetch('https://api.stripe.com/v1/accounts', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${stripeKey}`,
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: accParams.toString()
        });
        const account = await accRes.json();
        if (account.error) throw new Error(account.error.message);

        // 2. Create Account Onboarding Link
        const linkParams = new URLSearchParams();
        linkParams.append('account', account.id);
        linkParams.append('refresh_url', 'https://jooshoo11.github.io/swfl-holiday-planner/admin.html?stripe_refresh=true');
        linkParams.append('return_url', `https://jooshoo11.github.io/swfl-holiday-planner/admin.html?stripe_success=true&account_id=${account.id}`);
        linkParams.append('type', 'account_onboarding');

        const linkRes = await fetch('https://api.stripe.com/v1/account_links', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${stripeKey}`,
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: linkParams.toString()
        });
        const linkData = await linkRes.json();
        if (linkData.error) throw new Error(linkData.error.message);

        // Return JSON or redirect
        if (request.headers.get('Accept')?.includes('application/json')) {
          return new Response(JSON.stringify({ url: linkData.url, accountId: account.id }), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }

        return Response.redirect(linkData.url, 302);
      } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }
    }

    return new Response('Not Found', { status: 404, headers: corsHeaders });
  }
};
