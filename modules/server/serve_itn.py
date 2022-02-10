import json
import falcon
from datetime import datetime


class ServeITN:
    def on_post(self, request: falcon.Request, response: falcon.Response):
        inp: str = request.bounded_stream.read().decode()
        lang = request.get_param("lang")
        dig_en = request.get_param_as_bool("dig_en", default=False)

        output = {"input": inp, "lang": lang, "dig_en": dig_en}

        try:
            exec(f"from modules.langs.{lang} import ITN")
            out = ""
            lines = 0
            start_time = datetime.now()
            for line in inp.splitlines():
                out += eval(f"ITN().execute('{line}', dig_en={dig_en})") + "\n"
                lines += 1
            end_time = datetime.now()
            output["result"] = out.strip()
            output["lines"] = lines
            output["total_time_taken"] = f"{(end_time - start_time).seconds} seconds"
        except BaseException as e:
            print(e.args)
            output["err"] = "Error!"
        response.status = falcon.HTTP_OK
        response.content_type = falcon.MEDIA_JSON
        response.text = json.dumps(output)
