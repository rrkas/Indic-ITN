import json
import falcon
from datetime import datetime
from modules.langs import lang_map
import traceback


class ServeITN:
    def on_post(self, request: falcon.Request, response: falcon.Response):
        inp: str = request.bounded_stream.read().decode()
        lang = request.get_param("lang")
        dig_en = request.get_param_as_bool("dig_en", default=False)

        output = {"input": inp, "lang": lang, "dig_en": dig_en}

        try:
            if not (lang in lang_map):
                raise Exception(
                    f"{lang} not valid or not yet available!",
                    f"available langs: {list(lang_map.keys())}",
                )
            itn = lang_map[lang]
            out = ""
            lines = 0
            start_time = datetime.now()
            for line in inp.splitlines():
                out += itn.execute(line, dig_en=dig_en) + "\n"
                lines += 1
            end_time = datetime.now()
            output["result"] = out.strip()
            output["lines"] = lines
            output["total_time_taken"] = f"{(end_time - start_time).seconds} seconds"
        except BaseException as e:
            traceback.print_exc()
            output["err"] = " ".join(e.args)
        response.status = falcon.HTTP_OK
        response.content_type = falcon.MEDIA_JSON
        response.text = json.dumps(output)
