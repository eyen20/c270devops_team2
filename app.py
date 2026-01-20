from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

PORT = 8000

def load_expenses():
    with open("expenses.json", "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f)

class ExpenseHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            expenses = load_expenses()

            expense_html = "<ul>"
            for e in expenses:
                expense_html += f"<li>{e['title']} - ${e['amount']}</li>"
            expense_html += "</ul>"

            with open("index.html") as f:
                html = f.read().replace("{{expenses}}", expense_html)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode()
        form = urllib.parse.parse_qs(data)

        expense = {
            "title": form["title"][0],
            "amount": form["amount"][0]
        }

        expenses = load_expenses()
        expenses.append(expense)
        save_expenses(expenses)

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), ExpenseHandler)
    print(f"Server running at http://localhost:{PORT}")
    server.serve_forever()
