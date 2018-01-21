import webapp2
import httplib, urllib
import StringIO
import threading
from google.appengine.ext.webapp import template


FILENAME = 'digits.csv'


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(template.render('main.html', {}))

    def post(self):
        digits = str(self.request.get('file')).split()
        output_data = []
        count_thread = 3
        place_thread = 0
        for thread in range(0, count_thread):
            if thread == count_thread - 1:
                digits_thread = threading.Thread(target=search_digit, args=(digits[place_thread:len(digits)], output_data, ))
            else:
                digits_thread = threading.Thread(target=search_digit, args=(digits[place_thread:place_thread+int(len(digits)/count_thread)], output_data, ))
            digits_thread.start()
            digits_thread.join()
            place_thread += int(len(digits)/count_thread)
        output = StringIO.StringIO()
        for digit in output_data:
            for num in range(0, len(digit)):
                output.write(digit[num])
                output.write(',')
            output.write('\n')
        self.response.headers.add("Content-disposition", 'attachment; filename=filename.csv')
        self.response.write(output.getvalue())


def search_digit(digits, output):
    for digit in digits:
        about_digit_list = post_digit(digit).replace('[', '').replace(']', '').split(',')
        if about_digit_list[0].isdigit():
            output.append([int(digit), str(False), about_digit_list[0] + '+' + about_digit_list[1] + '+' + about_digit_list[2], about_digit_list[3] + '+' + about_digit_list[4] + '+' + about_digit_list[5], float(about_digit_list[6])])
        else:
            output.append([int(digit), about_digit_list[0], None, None, float(about_digit_list[1])])
    return output


def post_digit(digit):
    params = urllib.urlencode({'digit': digit})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("primes-192101.appspot.com")
    conn.request("POST", "", params, headers)
    response = conn.getresponse()
    return response.read()


app = webapp2.WSGIApplication([('/', MainPage), ], debug=True)