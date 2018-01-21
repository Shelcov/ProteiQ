import webapp2
import time


class MainPage(webapp2.RequestHandler):
	def post(self):
		start_time = time.time()
		status = self.request.POST['digit']
		sost = main_prime(int(status))
		end_time = time.time()
		self.response.write([sost, round((end_time - start_time) * 1000, 3)])
		
	def get(self):
		self.response.write(self.request)
        
       
def is_prime(digit):
    if digit > 3 and digit % 2 == 0 or digit <= 1:
        return False
    for i in range(3, int(digit ** 0.5) + 1, 2):
        if digit % i == 0:
            return False
    return True


def sum_prime(digit, start):
    prime_list = []
    for number in range(start-1, 1, -1):
        if is_prime(number):
            for number_prime in range(2, number):
                if is_prime(number_prime) and number + number_prime < digit:
                    for number_prime_second in range(2, number):
                        if is_prime(number_prime_second) and number + number_prime + number_prime_second == digit:
                            prime_list.append(number)
                            prime_list.append(number_prime)
                            prime_list.append(number_prime_second)
                            return prime_list


def main_prime(digit):
    status_prime = is_prime(digit)
    if not status_prime and digit > 20:
        list1 = sum_prime(digit, digit)
        list2 = sum_prime(digit, list1[0])
        return list1 + list2
    else:
        return status_prime


app = webapp2.WSGIApplication([('/', MainPage), ], debug=True)