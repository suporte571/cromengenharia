import json,urllib.request,urllib.error,base64,re,os
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
auth=re.search(r'user = "(.*)"',open(f'{S}/wp.netrc.cfg').read()).group(1)
H={'Authorization':'Basic '+base64.b64encode(auth.encode()).decode(),'Content-Type':'application/json','User-Agent':'Mozilla/5.0 crom-seo'}
def req(method,path,data=None):
  r=urllib.request.Request('https://cromengenharia.com/wp-json/'+path,data=json.dumps(data).encode() if data is not None else None,headers=H,method=method)
  try: return json.load(urllib.request.urlopen(r,timeout=120))
  except urllib.error.HTTPError as e: return {'HTTPError':e.code,'body':e.read().decode()[:400]}
