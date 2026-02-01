---
name: create_elite_article
description: Creates a high-value, SEO-optimized article for Elite Fashion, ensuring deep content, premium aesthetics, and complete social sharing tags.
---

# Skill: Create Elite Article

This skill encapsulates the editorial standards for creating "Deep Long-form" content for the Elite Fashion brand. Use this skill whenever the user requests a new article or series of articles.

## 1. Preparation Phase
- **Consult Editorial Guidelines**: Understand the core objective: High-Value Affiliate Monetization.
- **Audience Targeting**: Focus on High-Net-Worth Individuals (HNWIs) in Taiwan/Asia.
- **SEO Research**: Identify high commercial intent keywords (e.g., "Best...", "Review", "Guide").
- **Title Selection**: Create a compelling H1 that includes the current year (e.g., "2026") and a strong promise or benefit.

## 2. Content Structure (Deep Long-form)
- **Word Count**: Target 2,500+ words (or sufficient depth to dominate SEO).
- **Hierarchy**: Use strict `H1 -> H2 -> H3 -> H4 -> H5` nesting.
- **Essential Elements**:
    -   **Data Tables**: MUST include at least one CSS-styled comparison table (Product A vs Product B).
    -   **Expert Quotes**: Use real or realistic industry quotes to build authority.
    -   **Local Context**: MUST reference Taiwan (Taipei, Xinyi District, Dcard, PTT) to build trust.
    -   **Affiliate CTAs**: Place distinct, professional buttons (e.g., "View Offer", "Check Price") after product mentions.

## 3. Visual & Aesthetic Standards
- **Cover Image**:
    -   Use `curl` to download a high-quality, relevant stock photo from `loremflickr.com` or similar.
    -   AVOID repetitive AI-generated style if possible; prefer realistic photography.
    -   Image Path: `images/generated/ai/[filename].png` (or appropriate category folder).
- **Styling**:
    -   Font: `Playfair Display` for headers (Luxury), `Inter` for body (Readability).
    -   Spacing: Use generous whitespace (`line-height: 1.8`, padding).
    -   Color Palette: Adhere to the brand's premium palette (Gold, Dark Grey, White).

## 4. Technical Requirements (Critical)
- **Meta Tags**:
    -   `description`: Compelling summary for SERP (Search Engine Results Page).
    -   `keywords`: 5-8 relevant tags.
- **Open Graph (Social Sharing) - NON-NEGOTIABLE**:
    -   `og:type`: `article`
    -   `og:title`: Same as page title.
    -   `og:description`: Same as meta description.
    -   `og:url`: Full absolute URL (e.g., `https://mkhsu2002.github.io/elitefashiontw/...`).
    -   `og:image`: Full absolute URL to the cover image. **This is crucial for social sharing.**

## 5. Implementation Steps
1.  **Drafting**: Write the HTML content following the structure above.
2.  **Image Sourcing**: Download the cover image.
3.  **Review**: Verify all tags (especially OG tags) and local context references.
4.  **Integration**: Add the new article card to the relevant landing page grid.
5.  **Commit**: Git commit with a descriptive message.

## Example HTML Structure
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>Article Title | Elite Fashion</title>
    <meta name="description" content="...">
    <meta name="keywords" content="...">
    <!-- Open Graph Tags -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="...">
    <meta property="og:description" content="...">
    <meta property="og:url" content="...">
    <meta property="og:image" content="...">
    <link rel="stylesheet" href="../css/styles.css">
    <!-- Fonts & Styles -->
    ...
</head>
<body>
    <!-- Navbar -->
    <div class="article-container">
        <!-- Meta Info -->
        <!-- Image -->
        <!-- Content -->
    </div>
    <!-- Footer -->
</body>
</html>
```
