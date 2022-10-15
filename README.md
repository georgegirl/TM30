PROJECT EXPLANATION
ENDPOINTS:

CATEGORY ENDPOINT:
Each endpoint point to various aspect of the mrs Favours retail business. The category api point to the various items the retail business have in their inventory, which has grains& cerals, brews and juice, chocolate, candy, protein to name a few.
The get endpoint provides all the the category of products the have. 
The post endpoint provides ability to the admin (mrs favour) to add to the category od product they have
The delete endpoint provides ability to delete any category which is only accessable to the admin.


THE PRODUCT ENDPOINT:
The Product endpoint provides ability to the user and admin to access the product of mrs favours inventory. The get endpoint provides access to both the user and the admin to get product stated in the database.
The post endpoint is accessable to the admin. it used to post product to add to the inventory.
The put endpoint is accessable to the admin. it used to change a certain aspect of the product such as the quantity in stock or the price of the product.
The delete endpoint provides ability to delete products in the database only the admin can do.


THE CART ENDPOINT:
The CART endpoint provides ability to the user to access the various product available in mrs favours retail business.
The cart endpoint provides access to the login user to the cart product added to his cart and identifies if he is done his shopping cart, and also the logged in user also ability to change the status of the cart, showing his done with shopping and ready to purchase the listed product.

The permissions such as the IsAdmin, IsUser was written by me. 
IsAdmin: provides access to only the admin which is the superUser.
IsUser: provides access to the user who is logged in and has been authenticated. each before authentication,users are sent refresh token and token in order to access their account. 




To Access the Database:
USERNAME: Gloria
PASSWORD: ikpemosime




