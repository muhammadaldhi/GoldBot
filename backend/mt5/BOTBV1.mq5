#property strict

#include <Trade/Trade.mqh>


CTrade trade;


string API_URL = "http://127.0.0.1:5000";


int TIMER_SECONDS = 5;



//====================================================
// INIT
//====================================================

int OnInit()
{

   Print("BOTBV1 Started");


   SendConnect();


   EventSetTimer(
      TIMER_SECONDS
   );


   return(INIT_SUCCEEDED);

}



//====================================================
// DEINIT
//====================================================

void OnDeinit(
   const int reason
)
{

   EventKillTimer();

}



//====================================================
// TIMER
//====================================================

void OnTimer()
{

   SendTick();


   CheckOrder();

}



//====================================================
// CONNECT
//====================================================

void SendConnect()
{

   string json =
   "{"
   "\"ea\":\"BOTBV1\","
   "\"symbol\":\"XAUUSD\""
   "}";


   SendRequest(
      API_URL + "/mt5/connect",
      json
   );

}



//====================================================
// SEND TICK
//====================================================

void SendTick()
{

   double bid =
   SymbolInfoDouble(
      "XAUUSD",
      SYMBOL_BID
   );


   double ask =
   SymbolInfoDouble(
      "XAUUSD",
      SYMBOL_ASK
   );


   string json =
   "{"
   "\"symbol\":\"XAUUSD\","
   "\"bid\":"+
   DoubleToString(
      bid,
      2
   )
   +
   ","
   "\"ask\":"+
   DoubleToString(
      ask,
      2
   )
   +
   "}";


   SendRequest(
      API_URL + "/mt5/tick",
      json
   );

}



//====================================================
// CHECK ORDER QUEUE
//====================================================

void CheckOrder()
{

   string url =
   API_URL + "/mt5/order";


   char data[];
   char result[];

   string headers =
   "Content-Type: application/json\r\n";


   string response_headers;



   int code =
   WebRequest(
      "GET",
      url,
      headers,
      5000,
      data,
      result,
      response_headers
   );



   if(code != 200)
   {

      Print(
         "Order request failed ",
         GetLastError()
      );

      return;

   }



   string response =
   CharArrayToString(
      result
   );



   Print(
      "Order response: ",
      response
   );



   if(
      StringFind(
         response,
         "\"status\":\"empty\""
      )
      >=0
   )
   {

      return;

   }



   int id =
   GetIntValue(
      response,
      "id"
   );


   string action =
   GetStringValue(
      response,
      "action"
   );


   string symbol =
   GetStringValue(
      response,
      "symbol"
   );


   double lot =
   GetDoubleValue(
      response,
      "lot"
   );



   Print(
      "Execute ",
      action,
      " ",
      symbol,
      " ",
      lot
   );



   bool success=false;



   if(action=="BUY")
   {

      success =
      trade.Buy(
         lot,
         symbol
      );

   }



   if(action=="SELL")
   {

      success =
      trade.Sell(
         lot,
         symbol
      );

   }



   if(success)
   {

      SendOrderDone(
         id
      );

   }
   else
   {

      SendOrderFailed(
         id
      );

   }

}



//====================================================
// CALLBACK DONE
//====================================================

void SendOrderDone(
   int id
)
{

   string url =
   API_URL
   +
   "/mt5/order/"
   +
   IntegerToString(id)
   +
   "/done";


   SendRequest(
      url,
      "{}"
   );

}



//====================================================
// CALLBACK FAILED
//====================================================

void SendOrderFailed(
   int id
)
{

   string url =
   API_URL
   +
   "/mt5/order/"
   +
   IntegerToString(id)
   +
   "/failed";


   SendRequest(
      url,
      "{}"
   );

}



//====================================================
// HTTP POST
//====================================================

void SendRequest(
   string url,
   string json
)
{

   char data[];
   char result[];


   string headers =
   "Content-Type: application/json\r\n";


   string response_headers;



   StringToCharArray(
      json,
      data,
      0,
      StringLen(json)
   );



   int res =
   WebRequest(
      "POST",
      url,
      headers,
      5000,
      data,
      result,
      response_headers
   );



   if(res==-1)
   {

      Print(
         "WebRequest error: ",
         GetLastError()
      );

   }

}



//====================================================
// SIMPLE JSON PARSER
//====================================================

string GetStringValue(
   string json,
   string key
)
{

   string search =
   "\""
   +
   key
   +
   "\":\"";


   int start =
   StringFind(
      json,
      search
   );


   if(start<0)
      return "";



   start += StringLen(search);



   int end =
   StringFind(
      json,
      "\"",
      start
   );


   return StringSubstr(
      json,
      start,
      end-start
   );

}



int GetIntValue(
   string json,
   string key
)
{

   return(
      (int)GetDoubleValue(
         json,
         key
      )
   );

}



double GetDoubleValue(
   string json,
   string key
)
{

   string search =
   "\""
   +
   key
   +
   "\":";


   int start =
   StringFind(
      json,
      search
   );


   if(start<0)
      return 0;



   start += StringLen(search);



   int end=start;



   while(
      end<StringLen(json)
   )
   {

      string c =
      StringSubstr(
         json,
         end,
         1
      );


      if(
         c=="," ||
         c=="}"
      )
         break;


      end++;

   }



   string value =
   StringSubstr(
      json,
      start,
      end-start
   );


   return(
      StringToDouble(
         value
      )
   );

}