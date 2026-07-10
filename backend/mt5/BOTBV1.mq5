#property strict

#include <Trade/Trade.mqh>

CTrade trade;


input long MagicNumber = 777001;


string API_URL = "http://127.0.0.1:5000";


int TIMER_SECONDS = 5;



//====================================================
// INIT
//====================================================

int OnInit()
{

   Print("BOTBV1 Started");


   trade.SetExpertMagicNumber(
      MagicNumber
   );


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

   SendPositions();

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
// TICK
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
   DoubleToString(bid,2)
   +
   ","
   "\"ask\":"+
   DoubleToString(ask,2)
   +
   "}";


   SendRequest(
      API_URL + "/mt5/tick",
      json
   );

}



//====================================================
// GET ORDER
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
      return;



   string response =
   CharArrayToString(
      result
   );


   if(
      StringFind(
         response,
         "\"status\":\"empty\""
      ) >= 0
   )
      return;



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


   double volume =
   GetDoubleValue(
      response,
      "volume"
   );


   double sl =
   GetDoubleValue(
      response,
      "sl"
   );


   double tp =
   GetDoubleValue(
      response,
      "tp"
   );



   bool success=false;



   if(action=="BUY")
   {

      success =
      trade.Buy(
         volume,
         symbol,
         0,
         sl,
         tp,
         "GoldBot"
      );

   }


   if(action=="SELL")
   {

      success =
      trade.Sell(
         volume,
         symbol,
         0,
         sl,
         tp,
         "GoldBot"
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
// SEND ORDER DONE
//====================================================

void SendOrderDone(
   int id
)
{

   ulong ticket =
   trade.ResultOrder();


   string json =
   "{"
   "\"ticket\":"
   +
   IntegerToString(
      ticket
   )
   +
   "}";


   SendRequest(
      API_URL
      +
      "/mt5/order/"
      +
      IntegerToString(id)
      +
      "/done",

      json
   );

}



//====================================================
// SEND FAILED
//====================================================

void SendOrderFailed(
   int id
)
{

   SendRequest(

      API_URL
      +
      "/mt5/order/"
      +
      IntegerToString(id)
      +
      "/failed",

      "{\"error\":\"Order failed\"}"

   );

}



//====================================================
// POSITION SYNC
//====================================================
void SendPositions()
{

   string json = "[";

   bool first = true;


   int total = PositionsTotal();


   for(
      int i=0;
      i<total;
      i++
   )
   {

      ulong ticket =
      PositionGetTicket(i);


      if(
         !PositionSelectByTicket(ticket)
      )
         continue;



      if(!first)
      {
         json += ",";
      }


      first = false;



      string type =
      PositionGetInteger(
         POSITION_TYPE
      ) == POSITION_TYPE_BUY
      ?
      "BUY"
      :
      "SELL";



      json += "{";

      json += "\"ticket\":"+
      IntegerToString(ticket)+",";


      json += "\"symbol\":\""+
      PositionGetString(
         POSITION_SYMBOL
      )
      +"\",";


      json += "\"type\":\""+
      type
      +"\",";


      json += "\"volume\":"+
      DoubleToString(
         PositionGetDouble(
            POSITION_VOLUME
         ),
         2
      )
      +",";


      json += "\"price_open\":"+
      DoubleToString(
         PositionGetDouble(
            POSITION_PRICE_OPEN
         ),
         5
      )
      +",";


      json += "\"price_current\":"+
      DoubleToString(
         PositionGetDouble(
            POSITION_PRICE_CURRENT
         ),
         5
      )
      +",";


      json += "\"sl\":"+
      DoubleToString(
         PositionGetDouble(
            POSITION_SL
         ),
         5
      )
      +",";


      json += "\"tp\":"+
      DoubleToString(
         PositionGetDouble(
            POSITION_TP
         ),
         5
      )
      +",";


      json += "\"profit\":"+
      DoubleToString(
         PositionGetDouble(
            POSITION_PROFIT
         ),
         2
      )
      +",";


      json += "\"swap\":"+
      DoubleToString(
         PositionGetDouble(
            POSITION_SWAP
         ),
         2
      )
      +",";


      json += "\"commission\":0,";


      json += "\"magic\":"+
      IntegerToString(
         PositionGetInteger(
            POSITION_MAGIC
         )
      )
      +",";


      json += "\"comment\":\""+
      PositionGetString(
         POSITION_COMMENT
      )
      +"\"";


      json += "}";

   }


   json += "]";


   Print(
      "Position JSON: ",
      json
   );


   SendRequest(
      API_URL+"/mt5/positions",
      json
   );

}



//====================================================
// HTTP POST
//====================================================

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



   int size =
   StringToCharArray(
      json,
      data,
      0,
      WHOLE_ARRAY,
      CP_UTF8
   );


   // buang NULL terminator
   if(size > 0)
   {
      ArrayResize(
         data,
         size - 1
      );
   }



   int code =
   WebRequest(
      "POST",
      url,
      headers,
      5000,
      data,
      result,
      response_headers
   );



   Print(
      "POST ",
      url,
      " HTTP CODE=",
      code
   );


   if(code != 200)
   {

      Print(
         "WebRequest error: ",
         GetLastError()
      );

   }


   string response =
   CharArrayToString(
      result
   );


   Print(
      "Response: ",
      response
   );

}


//====================================================
// JSON STRING
//====================================================

string GetStringValue(
   string json,
   string key
)
{

   string search =
   "\""+key+"\":\"";


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



//====================================================
// JSON NUMBER
//====================================================

double GetDoubleValue(
   string json,
   string key
)
{

   string search =
   "\""+key+"\":" ;


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


      if(c=="," || c=="}")
         break;


      end++;

   }


   return StringToDouble(
      StringSubstr(
         json,
         start,
         end-start
      )
   );

}



int GetIntValue(
   string json,
   string key
)
{

   return (int)GetDoubleValue(
      json,
      key
   );

}