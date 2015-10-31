from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_apps.base import PersistentStore


class CuahsiDataCartDemo(TethysAppBase):
    """
    Tethys app class for CUAHSI Data Cart Demo.
    """

    name = 'CUAHSI Data Cart Demo'
    index = 'data_cart:home'
    icon = 'data_cart/images/icon.gif'
    package = 'data_cart'
    root_url = 'data-cart'
    color = '#e67e22'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='data-cart',
                           controller='data_cart.controllers.home'),
                    UrlMap(name='showfile',
                           url='showfile/{id}',
                           controller='data_cart.controllers.showfile'),
                    UrlMap(name='addfile',
                           url='addfile',
                           controller='data_cart.controllers.addfile')
        )

        return url_maps


    def persistent_stores(self):
        """
        Add one or more persistent stores
        """
        stores = (PersistentStore(name='datacart_db',
                                  initializer='init_stores:init_datacart_db',
                                  spatial=False
                                  ),
        )
        return stores