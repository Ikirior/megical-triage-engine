import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";


// this function must be named proxy
export async function proxy(req: NextRequest)
{
    // https://nextjs.org/docs/14/app/building-your-application/routing/middleware
    
    // https://timomeh.de/posts/if-youre-using-next-js-middleware-for-authorization-youre-doing-something-wrong
    // This middleware / proxy is meant solely for redirects, in case of expired access tokens
    // or unauthorized access with provided credentials. It does not authenticate, as that 
    // is done on the backend, which has the choice of returning unauthorized, triggering a redirect as well.

    // Requests to authenticate are done on the sign in / login page.

    const res = NextResponse.next()

    // https://nextjs.org/docs/app/api-reference/file-conventions/route#cookies
    const cookies_data = await cookies();

    if(cookies_data.has('session_token'))
    {
        //console.log('all set!', res.cookies.get('session_token'), cookies_data.get('session_token'))
    }
    else
        
    {
        //cookies_data.set('session_token', 'aaaaa.bbbbb.ccccc');
        return NextResponse.redirect(new URL('/login', req.url))

    }

    // Session token has been set. Proceed.
    // if(res.cookies.has('session_token'))
    // {
    //     console.log('all set!', res.cookies.get('session_token'))
    // }
    // // Session token is absent.
    // else 
    // {
    //     console.log('setting you up!')
    //     res.cookies.set('session_token', 'aaaaa.bbbbb.ccccc')
    //     return NextResponse.redirect(new URL('/login', req.url))
    // }
    return res
}

export const config = {
    matcher: ["/triagepanel/:path*"]
}