import drest
from flask import current_app as app
from drest.exc import dRestRequestError, dRestError

API_PATH = '/api/v1/'
MAX_ITEMS_PER_REQUEST = 100

class UnauthorizedError(Exception):
    pass

class NotFoundError(Exception):
    pass

def extract_error_messages(exc):
    if not hasattr(exc, 'response') or 'errors' not in exc.response.data:
        return
    return '; '.join([x['message'] for x in exc.response.data['errors']])

class CanvasApi(drest.API):

    def __init__(self, canvas_base_url, access_token):
        self.canvas_base_url = canvas_base_url
        self.access_header = {'Authorization': "Bearer %s" % access_token}
        super(CanvasApi, self).__init__(canvas_base_url + API_PATH,
                                        extra_headers=self.access_header,
                                        extra_url_params={'per_page': 1000},
                                        timeout=60,
                                        serialize=True,
                                        trailing_slash=False)

    def get_module_data(self, course_id, module_id=None):
        if module_id is None:
            modules_path = '/courses/%d/modules/' % course_id

            try:
                resp = self.make_request('GET', modules_path)
                module_id = resp.data[0]['id']
            except IndexError:
                raise NotFoundError("No modules found for course %s" % course_id)
            except dRestRequestError, e:
                if '401' in e.msg:
                    raise UnauthorizedError(extract_error_messages(e))
                elif '404' in e.msg:
                    raise NotFoundError(extract_error_messages(e))
                else:
                    raise

        items_path = '/courses/%d/modules/%d/items' % (course_id, module_id)
        try:
            resp = self.make_request('GET', items_path)
            return resp.data
        except dRestRequestError, e:
            if '401' in e.msg:
                raise UnauthorizedError(extract_error_messages(e))
            elif '404' in e.msg:
                raise NotFoundError(extract_error_messages(e))
            else:
                raise
