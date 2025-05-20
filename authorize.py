import requests
from lxml import etree

cookies = {
    'bm_mi': '5CB3090C6822FF051D6829597A32AD8E~YAAQJdgjFxr+csiWAQAArYlo6BsX2sJprUu0MWc3CG66crVr647Whn0y/lV06Lo9C8XepL30vW5p/Nd7QDdUAbuqoPaBIxD9yZUVNjE1TLaKvFp632BNVMIX5D3l0LR6jNNMWAMWigoIm6J6TXWoaCZez7JVT0vFWYb9E3sX38bxj4SiKF4DQcyc0jeyyHRR42CVG2Ikh+pzhxHZ4PGrTZXEdDsg532eVyW7w99rgYla0L6NQHyf0ajwy9ryaQe46RQ1DVB2yitTEHBMBnPLyZSnUGpyLt78oz5C5aDuUy4askW+BmPoVpVEKA8dPmeB~1',
    '_gcl_au': '1.1.1647554421.1747655890',
    '_ga': 'GA1.1.1078223496.1747655890',
    'ak_bmsc': '7E6F9B19C20FA02CEF6295BE8ED4E590~000000000000000000000000000000~YAAQJdgjF57+csiWAQAAk5Fo6Buq+kRDWClXJZdFvzTrT34tQD9gE7FzSzykEw5XPtZQDIlTeW0exSSF+2iCkwMi4EzOKd/doWJjB1QwjF+METSVFREJ+vi105fLYHcMOoF8BfPZpuBrAbtCC0VeeBc0YV+JXicjxZgJB1EcY7Ujzq4KwRNuhYvFD9BA3sd6rSQA3lG/qz+rXWgOSzsxElKNaDunjzaGAsvN9ZIzd4PM0UFz0f0QDWuVARJAReDih2eMZlpTXa+aSHoG17uDS+SUWAstF0HJQyOvrhqUqrw3PLM+eSImPTzJOsDN77S2mRpZ8qEnokNxTR6Quk7K2xFmu4QtlNm3lpTrytbDLwEYXr4hDpRwIFmRJi8pcUWpH3iu/Mk2sysAF69p7c61BpYmPG14iXQcg5HuSw9XHaUIceNmMZ14Gt7OatqezwOEqZGk7gcEBCfZfwIkCZtYOhslKMDfY19nNNZ74vsDH6wN',
    '_fbp': 'fb.1.1747655891008.318224823318290821',
    'cto_bundle': '2ysjQV9QZ3clMkI4bWIlMkJFa2ZvMml1b21yV2NFYmNTbVBWVVEzRHhPTmxKQ01YdXp1bmwwZ29adFdxbEgwTHdoR3UwSiUyRmpWMWxjVmNKdXZpU2N6cnlQVThzbXF4bEdHZExMVXNNd1VRMWhvWFlCcHYzJTJCMWxwVTVTV3JVYjhGTENWc2NMVlNa',
    '_ga_C9F0BWS8KH': 'GS2.1.s1747655890$o1$g1$t1747655945$j0$l0$h0',
    'SignInMessage.a41b6b2cd41eff4c5bf343d1b0030ac3': 'Ix3Kf446gctZMaWstVZIUc5uNM9GVO8vxKEy43s5iOJLrrJjiXDGM7_peLUJGT_u-TW3u8XfWjszI1JUZKEIsF4ssr7aXThij2i9OZJWCk0i4yXGWh4vMTJbmz5AWH6nK9XmIxGqQo2YHo-CdwyAf7mhHD0a_DEdey8T-wEeiLD8fbJVHGf-OzTB6pZJO5gDDGl5Fqukr97zSwfp-01N40Tu383YxeW8AXg8m57vi6KTv_1jHGRWdDpXnyBp5fXtZVLnw34R6caAeK_ZUoMTxYNiwhmz950vmHLB2UnRMQpPAWAMb3GEz9WD1hxSs16ivE-dVyOL4hFucQGkWz_HxXRiul74s7OgXRyMdvu0jzTP66P4WnearltjwyirZR8geoJxxVJ-LA6fkhsFovWuV1aFKn_xNgbcu3kiedopl06jDkFkS6DocbaPfUqJZ_UOqKQGbbVblS8Upiu-RW7NG1MbS9FsEfo0vziSg4Kz4qlN_LWykJ8fg9yNr42aFd-mbpMHcdGxSzdJ1a9z4F5O-Rv2nXX9Chp41sXlgybaiejw5XwuWlV1jvIbp_a9VWsY0QdjXGHdNNpLJmSvED9Ho35BGTINTxaONoUckMH4nDf9-zFz_UD0sgQMZbo1uz823Xh4lmdNVy5wia3kwr9OZw',
    'centralauthn.pending': 'RWFfAxfp317fIPaXvtG0i91o5cY30w0yK7mVHNdDDdeS0E5cBRoiqYPBfpa1Bb4a_2e2FBr1UN4sStYxEBItURdbYOQYwRofD7S7pdR1PMQNg_BAgMDj555XqjI8kQxIzH4Zwa-dBDnvBlgDLK6qhzMCMb3xJfxRLopLweLQzYDv-8tpHAQsemH1-VhjHKcI6JpzEPHiW-ioPOlDjwVsb3BmDMgKszYEqkX_DWR4HvYROzPu2yxTVKz019d2jIVdkIrdIFe_XDw8Zpb0jegq4mW7ymVy7PDbkGCoHvUcAfM',
    'idsrv.xsrf': 'bYoji2k4ikDyrBTDqw0c7jRPjVvDYto6vLLjDZldhaVq2kJC8Bw2LnW1LBT4ox3cnu34xIJwWudxkhnhbkSw66LjsUoIOYpUJal03hlZSa8',
    '__ssid': '4ba77515b324c2b304d368f5e139be5',
    'pc': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxTTHVmSWJfSUtRX29KLXVlcnR5MnBOS3o3QSIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIwNWJiNjZkNDI5NWU0NTEzODYyMDY1MDRlN2U0OGFjNSIsIm4iOiJkNGNmMGY2ZGVlMTk0ZTc5YmU1ZjZjN2FhNjk0MzE0ZSIsImV4cCI6MTgxMDcyOTI0MCwiaXNzIjoiaHR0cHM6Ly9zZWN1cmUuY29zdGFyZ3JvdXAuY29tIiwiYXVkIjoicGMifQ.hdNAQv4l2Bdj1uY8N8fp97izcVTCCkUmnlQMeTiVrgnUIfm6l1vfDX0hjU9pdaU_iIx9B9Wf2i4SCSGxSlm-yB-ONv9a8eyJ6lK5BBQLyCYqeo7zzlavy7wCEVP3jqNpyIwvFGkTdyEskdPMyZ1AnROqUq6JD9jCHB8N4mK77xdb5Lmv0BjzF0gUFMzlxZTKmMzDiHDqabC9DCxPgd0lQo0lmsWRT6fdUKw1ah8IKmxGYYNgYuwiPRRFe9rZLTtVVIxMrNluG1cxVFtbQivTOouerqmJ7998tP3IBJP6bXjVwLWVjrTbrg76NzMvxCXiJbrsLc4IPVfotpiyAPlsdA',
    'bm_sv': '7FF31353A079F1CC9B0D6C90BB869869~YAAQJdgjFy2adMiWAQAAPS996Bv7Hl5CKKUiIgMOroijrk9+ojRPG9N21pJ4fRuhXQoSpA6qSsE/vIbPfRP2iIhD1Voa9e69D9ayXuMUW1DZrJQlJtt3DWNWTqkDC/CY9wERPNR79MCHUmTPjPk9uItVfG7me8bT50a7EudTf1FjTiC9qcXwrslypCeiwgqU0NRQu3NJcN3fJVKucnnraILJ5h7nxMlgV7s2XhZUZ2My6rrzgfS9+LbpobwL6Et16GgvgjY=~1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.costar.com/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': 'bm_mi=5CB3090C6822FF051D6829597A32AD8E~YAAQJdgjFxr+csiWAQAArYlo6BsX2sJprUu0MWc3CG66crVr647Whn0y/lV06Lo9C8XepL30vW5p/Nd7QDdUAbuqoPaBIxD9yZUVNjE1TLaKvFp632BNVMIX5D3l0LR6jNNMWAMWigoIm6J6TXWoaCZez7JVT0vFWYb9E3sX38bxj4SiKF4DQcyc0jeyyHRR42CVG2Ikh+pzhxHZ4PGrTZXEdDsg532eVyW7w99rgYla0L6NQHyf0ajwy9ryaQe46RQ1DVB2yitTEHBMBnPLyZSnUGpyLt78oz5C5aDuUy4askW+BmPoVpVEKA8dPmeB~1; _gcl_au=1.1.1647554421.1747655890; _ga=GA1.1.1078223496.1747655890; ak_bmsc=7E6F9B19C20FA02CEF6295BE8ED4E590~000000000000000000000000000000~YAAQJdgjF57+csiWAQAAk5Fo6Buq+kRDWClXJZdFvzTrT34tQD9gE7FzSzykEw5XPtZQDIlTeW0exSSF+2iCkwMi4EzOKd/doWJjB1QwjF+METSVFREJ+vi105fLYHcMOoF8BfPZpuBrAbtCC0VeeBc0YV+JXicjxZgJB1EcY7Ujzq4KwRNuhYvFD9BA3sd6rSQA3lG/qz+rXWgOSzsxElKNaDunjzaGAsvN9ZIzd4PM0UFz0f0QDWuVARJAReDih2eMZlpTXa+aSHoG17uDS+SUWAstF0HJQyOvrhqUqrw3PLM+eSImPTzJOsDN77S2mRpZ8qEnokNxTR6Quk7K2xFmu4QtlNm3lpTrytbDLwEYXr4hDpRwIFmRJi8pcUWpH3iu/Mk2sysAF69p7c61BpYmPG14iXQcg5HuSw9XHaUIceNmMZ14Gt7OatqezwOEqZGk7gcEBCfZfwIkCZtYOhslKMDfY19nNNZ74vsDH6wN; _fbp=fb.1.1747655891008.318224823318290821; cto_bundle=2ysjQV9QZ3clMkI4bWIlMkJFa2ZvMml1b21yV2NFYmNTbVBWVVEzRHhPTmxKQ01YdXp1bmwwZ29adFdxbEgwTHdoR3UwSiUyRmpWMWxjVmNKdXZpU2N6cnlQVThzbXF4bEdHZExMVXNNd1VRMWhvWFlCcHYzJTJCMWxwVTVTV3JVYjhGTENWc2NMVlNa; _ga_C9F0BWS8KH=GS2.1.s1747655890$o1$g1$t1747655945$j0$l0$h0; SignInMessage.a41b6b2cd41eff4c5bf343d1b0030ac3=Ix3Kf446gctZMaWstVZIUc5uNM9GVO8vxKEy43s5iOJLrrJjiXDGM7_peLUJGT_u-TW3u8XfWjszI1JUZKEIsF4ssr7aXThij2i9OZJWCk0i4yXGWh4vMTJbmz5AWH6nK9XmIxGqQo2YHo-CdwyAf7mhHD0a_DEdey8T-wEeiLD8fbJVHGf-OzTB6pZJO5gDDGl5Fqukr97zSwfp-01N40Tu383YxeW8AXg8m57vi6KTv_1jHGRWdDpXnyBp5fXtZVLnw34R6caAeK_ZUoMTxYNiwhmz950vmHLB2UnRMQpPAWAMb3GEz9WD1hxSs16ivE-dVyOL4hFucQGkWz_HxXRiul74s7OgXRyMdvu0jzTP66P4WnearltjwyirZR8geoJxxVJ-LA6fkhsFovWuV1aFKn_xNgbcu3kiedopl06jDkFkS6DocbaPfUqJZ_UOqKQGbbVblS8Upiu-RW7NG1MbS9FsEfo0vziSg4Kz4qlN_LWykJ8fg9yNr42aFd-mbpMHcdGxSzdJ1a9z4F5O-Rv2nXX9Chp41sXlgybaiejw5XwuWlV1jvIbp_a9VWsY0QdjXGHdNNpLJmSvED9Ho35BGTINTxaONoUckMH4nDf9-zFz_UD0sgQMZbo1uz823Xh4lmdNVy5wia3kwr9OZw; centralauthn.pending=RWFfAxfp317fIPaXvtG0i91o5cY30w0yK7mVHNdDDdeS0E5cBRoiqYPBfpa1Bb4a_2e2FBr1UN4sStYxEBItURdbYOQYwRofD7S7pdR1PMQNg_BAgMDj555XqjI8kQxIzH4Zwa-dBDnvBlgDLK6qhzMCMb3xJfxRLopLweLQzYDv-8tpHAQsemH1-VhjHKcI6JpzEPHiW-ioPOlDjwVsb3BmDMgKszYEqkX_DWR4HvYROzPu2yxTVKz019d2jIVdkIrdIFe_XDw8Zpb0jegq4mW7ymVy7PDbkGCoHvUcAfM; idsrv.xsrf=bYoji2k4ikDyrBTDqw0c7jRPjVvDYto6vLLjDZldhaVq2kJC8Bw2LnW1LBT4ox3cnu34xIJwWudxkhnhbkSw66LjsUoIOYpUJal03hlZSa8; __ssid=4ba77515b324c2b304d368f5e139be5; pc=eyJhbGciOiJSUzI1NiIsImtpZCI6ImxTTHVmSWJfSUtRX29KLXVlcnR5MnBOS3o3QSIsInR5cCI6IkpXVCJ9.eyJ0aWQiOiIwNWJiNjZkNDI5NWU0NTEzODYyMDY1MDRlN2U0OGFjNSIsIm4iOiJkNGNmMGY2ZGVlMTk0ZTc5YmU1ZjZjN2FhNjk0MzE0ZSIsImV4cCI6MTgxMDcyOTI0MCwiaXNzIjoiaHR0cHM6Ly9zZWN1cmUuY29zdGFyZ3JvdXAuY29tIiwiYXVkIjoicGMifQ.hdNAQv4l2Bdj1uY8N8fp97izcVTCCkUmnlQMeTiVrgnUIfm6l1vfDX0hjU9pdaU_iIx9B9Wf2i4SCSGxSlm-yB-ONv9a8eyJ6lK5BBQLyCYqeo7zzlavy7wCEVP3jqNpyIwvFGkTdyEskdPMyZ1AnROqUq6JD9jCHB8N4mK77xdb5Lmv0BjzF0gUFMzlxZTKmMzDiHDqabC9DCxPgd0lQo0lmsWRT6fdUKw1ah8IKmxGYYNgYuwiPRRFe9rZLTtVVIxMrNluG1cxVFtbQivTOouerqmJ7998tP3IBJP6bXjVwLWVjrTbrg76NzMvxCXiJbrsLc4IPVfotpiyAPlsdA; bm_sv=7FF31353A079F1CC9B0D6C90BB869869~YAAQJdgjFy2adMiWAQAAPS996Bv7Hl5CKKUiIgMOroijrk9+ojRPG9N21pJ4fRuhXQoSpA6qSsE/vIbPfRP2iIhD1Voa9e69D9ayXuMUW1DZrJQlJtt3DWNWTqkDC/CY9wERPNR79MCHUmTPjPk9uItVfG7me8bT50a7EudTf1FjTiC9qcXwrslypCeiwgqU0NRQu3NJcN3fJVKucnnraILJ5h7nxMlgV7s2XhZUZ2My6rrzgfS9+LbpobwL6Et16GgvgjY=~1',
}

params = {
    'client_id': 'costar',
    'nonce': '1be7d3f4-3c90-4fdf-3472-433c2a19f11a',
    'response_type': 'code',
    'response_mode': 'form_post',
    'scope': 'openid profile email address phone offline_access product_user session',
    'redirect_uri': 'https://product.costar.com/home/auth-callback',
    'acr_values': '',
    'locale': 'en-US',
}

response = requests.get('https://secure.costargroup.com/connect/authorize', params=params, cookies=cookies, headers=headers)
# print(response.text)
# print(response)


tree = etree.HTML(response.text)
signinform = tree.xpath('//form[@id="signinform"]/@action')[0]
print(signinform) # /login?signin=11da2ea395f334add736d93e8c1b15ee

xsrf_token = tree.xpath('//input[@name="idsrv.xsrf"]/@value')[0]

print(xsrf_token)
