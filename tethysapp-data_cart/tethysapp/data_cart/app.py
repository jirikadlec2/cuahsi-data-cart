from tethys_sdk.base import TethysAppBase, url_map_maker


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