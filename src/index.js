export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Security headers
    const securityHeaders = {
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block',
      'Referrer-Policy': 'strict-origin-when-cross-origin',
      'Permissions-Policy': 'camera=(), microphone=(), geolocation=()'
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
