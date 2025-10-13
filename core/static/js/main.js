function slugify(text) {
  return text
    .toString()                              // Ensure it's a string
    .trim()                                  // Remove leading/trailing spaces
    .toLowerCase()                           // Lowercase for uniformity
    .replace(/[\u200B-\u200D\uFEFF]/g, '')   // Remove zero-width chars
    .replace(/[^\w\u0600-\u06FF\s-]/g, '')   // Keep Persian & English letters, digits, underscore, space, and dash
    .replace(/\s+/g, '-')                    // Replace spaces with -
    .replace(/-+/g, '-')                     // Merge multiple dashes
    .replace(/^-+|-+$/g, '');                // Trim - from start/end
}