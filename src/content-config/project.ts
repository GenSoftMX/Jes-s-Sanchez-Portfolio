import { z } from 'astro/zod';

export const projectSchema = z.object({
  projectId: z.string().min(1),
  language: z.enum(['es', 'en']),
  title: z.string().min(1),
  description: z.string().min(1),
  technologies: z.array(z.string().min(1)),
  links: z.array(z.object({ label: z.string().min(1), url: z.url() })),
  images: z.array(z.object({ src: z.string().min(1), alt: z.string().min(1) })).optional(),
  status: z.string().optional(),
  date: z.coerce.date().optional(),
});
