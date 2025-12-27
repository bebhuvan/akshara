export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Security headers
    const securityHeaders = {
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block',
      'Referrer-Policy': 'strict-origin-when-cross-origin',
      'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
      // HSTS - enforce HTTPS (1 year with preload)
      'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
      // COOP - isolate browsing context from cross-origin documents
      'Cross-Origin-Opener-Policy': 'same-origin',
      // CSP - prevent XSS and other injection attacks
      'Content-Security-Policy': [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self' https://cloudflareinsights.com",
        "frame-ancestors 'none'",
        "base-uri 'self'",
        "form-action 'self'"
      ].join('; ')
    };

    // Handle static assets (fonts, images, CSS, JS)
    if (url.pathname.startsWith('/static/') ||
        url.pathname.startsWith('/covers/') ||
        url.pathname.startsWith('/js/') ||
        url.pathname.startsWith('/fonts/') ||
        url.pathname.startsWith('/css/')) {

      const response = await env.ASSETS.fetch(request);

      // Cache static assets for 1 year
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'public, max-age=31536000, immutable');

      return new Response(response.body, {
        status: response.status,
        headers
      });
    }

    // Handle HTML pages
    if (url.pathname.endsWith('.html') || !url.pathname.includes('.')) {
      const response = await env.ASSETS.fetch(request);

      if (response.status === 404) {
        return env.ASSETS.fetch(new Request(new URL('/404.html', url)));
      }

      const headers = new Headers(response.headers);

      // Add security headers
      Object.entries(securityHeaders).forEach(([key, value]) => {
        headers.set(key, value);
      });

      // Cache HTML for 1 hour (can be purged)
      headers.set('Cache-Control', 'public, max-age=3600, must-revalidate');

      return new Response(response.body, {
        status: response.status,
        headers
      });
    }

    // Everything else
    return env.ASSETS.fetch(request);
  }
};
