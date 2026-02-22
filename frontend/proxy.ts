import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import {decode, JwtPayload, verify} from 'jsonwebtoken'

type token_type = {
    role: string,
    exp: number,
    sub: string
}

// this function must be named proxy
export async function proxy(req: NextRequest)
{
    // https://nextjs.org/docs/14/app/building-your-application/routing/middleware
    
    // https://timomeh.de/posts/if-youre-using-next-js-middleware-for-authorization-youre-doing-something-wrong
    // This middleware / proxy is meant solely for redirects, in case of expired access tokens
    // or unauthorized access with provided credentials. It does not authenticate, as that 
    // is done on the backend, which has the choice of returning unauthorized, triggering a redirect as well.

    // Requests to authenticate are done on the sign in / login page.
    // Authorization requests are done on every restricted access request

    const res = NextResponse.next()

    // https://nextjs.org/docs/app/api-reference/file-conventions/route#cookies
    const cookies_data = await cookies();


    const login_red = () => NextResponse.redirect(new URL('/login', req.url))

    if(cookies_data.has('session_token') && cookies_data.get('session_token')?.value)
    {
        // Validate token role
        const token = cookies_data.get('session_token')?.value
        if(token)
        {
            const decoded = decode(token) as token_type;
            const urlPath = new URL(req.url).pathname;
            if(
                (urlPath.startsWith('/adminpanel') && decoded.role != 'admin') ||
                (urlPath.startsWith('/triagepanel') && decoded.role != 'nurse') ||
                (urlPath.startsWith('/patientregistry') && decoded.role != 'receptionist')  
            )
            {
                console.log('<!> Proxy access redirected for insufficient role.')
                return login_red();
            }
        }
    }
    else 
    {
        console.log('<!> Proxy access redirected for inexistant token.')
        return login_red()
    }
    return res
}

export const config = {
    matcher: ["/triagepanel/:path*", "/adminpanel/:path*", "/patientregistry/:path*"]
}