Bol.com is a netherlands based website. The sellers can register on the website and sell there products. Once the product are sold the shipment details are available. 

This application will help in getting the shipment details for particular seller.

Steps to use the project:

1. Clone the repository
2. Install mariadb as database based on your operating system
3. Install mysql server
4. Install requirements.txt
5. Start mariadb server and create a database and user.
6. Open 2 different tabs in terminal and run the following commands:
  1. python manage.py runserver (make sure you are in the location of the manage.oy file)
  2. celery -A shipments worker --loglevel=info --autoscale=10,3 --max-tasks-per-child=10
7. Make requests from postman to test the APIs

Please feel free to comment and get in touch in case of any queries or feedbacks.
