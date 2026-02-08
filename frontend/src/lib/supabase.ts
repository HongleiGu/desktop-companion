import { createClient } from "@supabase/supabase-js";
// console.log(process.env.NEXT_PUBLIC_SUPABASE_URL)
export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
);
