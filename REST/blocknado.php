<?php

class BlocknadoREST {

  public $baseURL;
  private $_apiKey;
  private $_apiSecret;
  private $_nonce;
  private $_markets;
  private $_ch;

  public function __construct($apiKey, $apiSecret) {
    $this->baseURL = 'https://blocknado.com/api/v1';
    $this->_apiKey = $apiKey;
    $this->_apiSecret = $apiSecret;
    $this->_nonce = time();
    $this->_markets = array_map(function($market) { return $market['market']; }, $this->markets());
    $this->_ch = null;
    $this->setupCURL();
  }

  public function setupCURL() {
    if (is_null($this->_ch)) {
        $this->_ch = curl_init();
        curl_setopt($this->_ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($this->_ch, CURLOPT_USERAGENT, 'Blocknado PHP API Wrapper');
    }
    curl_setopt($this->_ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($this->_ch, CURLOPT_TIMEOUT, 10);
  }

  public function getMarkets() {
    return $this->_markets;
  }

  public function getCredentials() {
      return array($this->_apiKey, $this->_apiSecret);
  }

  public function checkCredentialsSet() {
      if(!$this->_apiKey || !$this->_apiSecret)
          return false;
      return true;
  }

  public function _getURL($call) {
      return sprintf("%s/%s", $this->baseURL, $call);
  }

  public function signData($params) {
      return hash_hmac('sha512', $params, $this->_apiSecret);
  }

  public function genHeaders($params) {
      return array(
          "User-Agent: Blocknado PHP API Wrapper",
          "Key: " .$this->_apiKey,
          "Sign: " .$this->signData($params)
      );
    }

  public function publicAPICall($call, $params=array()) {
      $this->setupCURL();
      $url = $this->_getURL($call);
      if(count($params) > 0)
          $url = sprintf("%s/%s", $url, implode('/', $params));
      curl_setopt($this->_ch, CURLOPT_URL, $url);
      curl_setopt($this->_ch, CURLOPT_SSL_VERIFYPEER, FALSE);
      curl_setopt($this->_ch, CURLOPT_TIMEOUT, 10);

      $res = curl_exec($this->_ch);
      if($res != false) {
          return json_decode($res, true);
      } else {
          return "Something went wrong";
      }
  }

  public function privateAPICall($call, $params=array()) {
      $this->setupCURL();
      if(!$this->checkCredentialsSet())
          die("Must provide an API Key and Secret");
      $params['nonce'] = $this->_nonce;
      $this->_nonce++;
      $params = http_build_query($params, '', '&');
      $headers = $this->genHeaders($params);
      $url = $this->_getURL($call);
      curl_setopt($this->_ch, CURLOPT_URL, $url);
      curl_setopt($this->_ch, CURLOPT_POSTFIELDS, $params);
      curl_setopt($this->_ch, CURLOPT_HTTPHEADER, $headers);
      curl_setopt($this->_ch, CURLOPT_SSL_VERIFYPEER, FALSE);
      curl_setopt($this->_ch, CURLOPT_TIMEOUT, 10);
      $res = curl_exec($this->_ch);

      if($res != false) {
          return json_decode($res, true);
      } else {
          return "Something went wrong";
      }
  }

  public function markets() {
      return $this->publicAPICall("markets");
  }

  public function orderbook($market) {
      if(!in_array(strtoupper($market), $this->_markets))
          die(sprintf("The selected market: %s does not exist", $market));
      return $this->publicAPICall("orderbook", array($market));
  }

  public function buy($market, $amount, $price) {
      return $this->privateAPICall('buy', array("market" => $market, "amount" => $amount, "price" => $price));
  }

  public function sell($market, $amount, $price) {
      return $this->privateAPICall('sell', array("market" => $market, "amount" => $amount, "price" => $price));
  }

  public function cancel($orderID) {
      return $this->privateAPICall('cancel', array("orderNumber" => $orderID));
  }

  public function open($market) {
      return $this->privateAPICall('open', array("market" => $market));
  }

  public function order($orderID) {
      return $this->privateAPICall('order', array("orderNumber" => $orderID));
  }

  public function balances() {
      return $this->privateAPICall('balances');
  }
}

?>
