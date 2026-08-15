import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_PATH = join(__dirname, "..", "data", "dataset.json");

export const GitHubIssueSchema = z.object({
  id: z.string(),
  number: z.number().int(),
  title: z.string(),
  body: z.string(),
  state: z.enum(["open", "closed"]),
  labels: z.array(z.string()),
  assignees: z.array(z.string()),
  author: z.string(),
  created_at: z.string(),
  closed_at: z.string().nullable().optional(),
  comments_count: z.number().int().min(0),
  reactions_count: z.number().int().min(0),
  milestone: z.string().nullable().optional(),
  pull_request: z.boolean(),
});

export const DatasetSchema = z.array(GitHubIssueSchema);
export type GitHubIssue = z.infer<typeof GitHubIssueSchema>;

export function loadAndValidate(): { valid: GitHubIssue[]; errors: z.ZodError[] } {
  const raw = JSON.parse(readFileSync(DATA_PATH, "utf-8"));
  const valid: GitHubIssue[] = [];
  const errors: z.ZodError[] = [];
  for (const item of raw) {
    const result = GitHubIssueSchema.safeParse(item);
    if (result.success) {
      valid.push(result.data);
    } else {
      errors.push(result.error);
    }
  }
  return { valid, errors };
}

export function validateRecord(record: unknown): record is GitHubIssue {
  return GitHubIssueSchema.safeParse(record).success;
}
