import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { neon } from "@neondatabase/serverless";

export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL,
  trustedOrigins: [process.env.BETTER_AUTH_URL ?? ""].filter(Boolean),
  database: neon(process.env.DATABASE_URL!),
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt({
      jwks: {
        keyPairConfig: {
          alg: "EdDSA",
          crv: "Ed25519",
        },
      },
    }),
  ],
});
