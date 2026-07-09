import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { PublicArticle } from "@/lib/types";

// Renders the article body. The backend returns body_format="markdown"; we render
// markdown safely with react-markdown (HTML is escaped, not injected). "plain" is
// shown as preformatted text. Unknown/"html" falls back to markdown rendering
// (still escaped) to avoid unsafe raw HTML injection from a non-trusted field.
export function ArticleBody({ article }: { article: PublicArticle }) {
  if (article.body_format === "plain") {
    return (
      <div className="prose prose-lg max-w-none whitespace-pre-wrap font-sans text-ink">
        {article.body}
      </div>
    );
  }
  return (
    <div className="prose prose-lg max-w-none prose-headings:font-serif prose-headings:text-ink prose-p:text-ink-soft prose-a:text-accent prose-strong:text-ink">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{article.body}</ReactMarkdown>
    </div>
  );
}
