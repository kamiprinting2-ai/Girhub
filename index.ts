// Seedance 2.5 text-to-video through the official Higgsfield SDK.
// Run: npm run higgsfield
// Credentials: HF_CREDENTIALS ("KEY_ID:KEY_SECRET") in .env.local, loaded at runtime.
// The value is never printed or logged here.
import { config as loadEnv } from "dotenv";
import {
  config,
  higgsfield,
  AuthenticationError,
  CredentialsMissedError,
  NotEnoughCreditsError,
  ValidationError,
  BadInputError,
  TimeoutError,
  APIError,
} from "@higgsfield/client/v2";

loadEnv({ path: ".env.local", quiet: true });

const MODEL = "bytedance/seedance-2.5/text-to-video";

if (!process.env.HF_CREDENTIALS) {
  console.error("HF_CREDENTIALS is not set in .env.local (expected KEY_ID:KEY_SECRET).");
  process.exit(1);
}

config({
  credentials: process.env.HF_CREDENTIALS,
  maxPollTime: 15 * 60 * 1000, // video can take longer than the 5 min default
});

async function main(): Promise<number> {
  console.log(`Submitting ${MODEL} ...`);
  const result = await higgsfield.subscribe(MODEL, {
    input: {
      prompt: "A cinematic scene at sunset",
      duration: 5,
      resolution: "720p",
      aspect_ratio: "16:9",
    },
    withPolling: true,
  });

  // The API may also report canceled; the SDK's type lists queued/in_progress/completed/failed/nsfw.
  const status = result.status as string;
  console.log(`Request ${result.request_id} finished with status: ${status}`);

  if (status === "completed") {
    const url = result.video?.url;
    if (!url) {
      console.error("Status is completed but the response has no video URL.");
      return 1;
    }
    console.log(`Video URL: ${url}`);
    return 0;
  }
  if (status === "nsfw") {
    console.error("The request was blocked by content moderation. No video was produced.");
  } else if (status === "failed") {
    console.error("The generation failed. No video was produced.");
  } else if (status === "canceled" || status === "cancelled") {
    console.error("The request was canceled. No video was produced.");
  } else {
    console.error(`Unexpected status "${status}". Not treating this as success.`);
  }
  return 1;
}

main()
  .then((code) => process.exit(code))
  .catch((err: unknown) => {
    if (err instanceof CredentialsMissedError) console.error("Credentials are missing.");
    else if (err instanceof AuthenticationError) console.error("Higgsfield rejected the credentials (401).");
    else if (err instanceof NotEnoughCreditsError) console.error("Not enough Higgsfield credits (403).");
    else if (err instanceof ValidationError || err instanceof BadInputError)
      console.error(`The request was rejected as invalid: ${err.message}`);
    else if (err instanceof TimeoutError)
      console.error("Polling timed out before a terminal status (the request may have been canceled or is still running).");
    else if (err instanceof APIError) console.error(`Higgsfield API error: ${err.message}`);
    else console.error(`Unexpected error: ${err instanceof Error ? err.message : String(err)}`);
    process.exit(1);
  });
