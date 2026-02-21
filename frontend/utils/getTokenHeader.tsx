'use server';

import { cookies } from "next/headers";

/**
 * Returns 'Bearer {token}'.
 */
export default async function getTokenHeaderValue() {
    return `Bearer ${(await cookies()).get('session_token')?.value}`
}