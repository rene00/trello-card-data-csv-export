Trello Card Export to CSV
=========================

Description
-----------

2 python scripts I hacked up which helped me pull in card data from
lists within Trello and export that card data to CSV.

I'm only interested in the name of the card and the short URL.

My cards have estimates embedded within the name it self.

For example:

.. code-block::

    (10) Build widget foo for feature bar.

* 10 is the point estimate.

* 'Build widget foo for feature bar.' is the name of the card.


How do I run this?
------------------

1. Install the `python trello package`_.


2. Grab your Trello key from https://trello.com/1/appKey/generate.

3. Grab a Trello Token URL.

.. code-block:: bash

    $ python get_token_url.py --trello-key ${TRELLO_KEY} \
        --prog-name my-app.py \
        --expires 30days \
        --write-access False

4. Go to the URL and 'Allow'.

5. Grab the token from the proceeding page.

6. Run get_card_data.py with the new token and the id of the list

.. code-block:: bash

    $ python get_card_data.py --trello-key ${TRELLO_KEY} \
        --list-id ${LIST_ID} \
        --trello-token ${TRELLO_TOKEN}

7. Check out the newly generated file ${LIST_ID}.csv.

The list ids of your boards are available via the 'export to JSON'
Trello board feature.

..  _python trello package: https://pypi.python.org/pypi/trello
