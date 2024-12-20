// List of common tracking parameters to remove
const TRACKING_PARAMS = new Set([
  // Google Analytics & Ads
  'utm_source',
  'utm_medium',
  'utm_campaign',
  'utm_term',
  'utm_content',
  'gclid',
  'gclsrc',
  // Facebook
  'fbclid',
  // Microsoft/Bing
  'msclkid',
  // Other common tracking parameters
  '_hsenc',
  '_hsmi',
  'mc_cid',
  'mc_eid',
  'zanpid',
  // Amazon
  'ref',
  'tag',
  // General
  'source',
  'affiliate',
  'campaign',
  'track'
]);

class URLCleaner {
  /**
   * Clean a URL by removing tracking parameters
   * @param {string} url - The URL to clean
   * @returns {string} - The cleaned URL
   */
  static clean(url) {
    try {
      const urlObj = new URL(url);
      const searchParams = new URLSearchParams(urlObj.search);
      let paramsRemoved = false;

      // Remove known tracking parameters
      for (const param of searchParams.keys()) {
        if (TRACKING_PARAMS.has(param.toLowerCase())) {
          searchParams.delete(param);
          paramsRemoved = true;
        }
      }

      // Remove any parameters that look like tracking IDs (common patterns)
      for (const param of searchParams.keys()) {
        if (this.looksLikeTrackingParam(param)) {
          searchParams.delete(param);
          paramsRemoved = true;
        }
      }

      // Reconstruct the URL
      urlObj.search = searchParams.toString();
      const cleanedUrl = urlObj.toString();

      // Remove trailing '?' if all parameters were removed
      return cleanedUrl.endsWith('?') ? cleanedUrl.slice(0, -1) : cleanedUrl;
    } catch (error) {
      console.error('Error cleaning URL:', error);
      return url; // Return original URL if there's an error
    }
  }

  /**
   * Check if a parameter name looks like a tracking parameter
   * @param {string} param - The parameter name to check
   * @returns {boolean} - True if the parameter looks like a tracking parameter
   */
  static looksLikeTrackingParam(param) {
    const trackingPatterns = [
      /^_.*id$/i,           // Parameters ending with 'id' with leading underscore
      /^ref_?.*$/i,         // Parameters starting with 'ref'
      /^track(ing)?_?.*$/i, // Parameters starting with 'track' or 'tracking'
      /^affiliate_?.*$/i,   // Parameters starting with 'affiliate'
      /^camp(aign)?_?.*$/i  // Parameters starting with 'camp' or 'campaign'
    ];

    return trackingPatterns.some(pattern => pattern.test(param));
  }

  /**
   * Clean multiple URLs at once
   * @param {string[]} urls - Array of URLs to clean
   * @returns {string[]} - Array of cleaned URLs
   */
  static cleanBatch(urls) {
    return urls.map(url => this.clean(url));
  }
}

// Example usage:
const dirtyUrl = 'https://example.com/product?id=123&utm_source=facebook&utm_medium=social&ref=share';
const cleanUrl = URLCleaner.clean(dirtyUrl);
console.log('Original URL:', dirtyUrl);
console.log('Cleaned URL:', cleanUrl);
