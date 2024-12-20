document.addEventListener('DOMContentLoaded', function() {
  const resultDiv = document.getElementById('result');
  
  // Clean current URL button
  document.getElementById('cleanCurrentUrl').addEventListener('click', async () => {
    const tabs = await browser.tabs.query({active: true, currentWindow: true});
    const currentUrl = tabs[0].url;
    const cleanedUrl = URLCleaner.clean(currentUrl);
    
    if (currentUrl !== cleanedUrl) {
      await navigator.clipboard.writeText(cleanedUrl);
      resultDiv.textContent = 'Cleaned URL copied to clipboard!';
      resultDiv.style.display = 'block';
    } else {
      resultDiv.textContent = 'No tracking parameters found.';
      resultDiv.style.display = 'block';
    }
  });
  
  // Clean from clipboard button
  document.getElementById('cleanFromClipboard').addEventListener('click', async () => {
    try {
      const clipboardText = await navigator.clipboard.readText();
      const cleanedUrl = URLCleaner.clean(clipboardText);
      
      await navigator.clipboard.writeText(cleanedUrl);
      resultDiv.textContent = 'Cleaned URL copied to clipboard!';
      resultDiv.style.display = 'block';
    } catch (error) {
      resultDiv.textContent = 'Error reading from clipboard';
      resultDiv.style.display = 'block';
    }
  });
});
