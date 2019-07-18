# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:58:19 2019

@author: RayomandVatcha
"""

GroupID = ["P2P", "224.1.1.1", "224.1.1.1","224.1.1.1","224.1.1.1", "224.1.1.1", "224.1.1.1","224.1.1.1","224.1.1.1", "224.1.1.1"]
key = ["16digitNo","16digitNo1234567", "16digitNo1234567","16digitNo1234567","16digitNo1234567","16digitNo1234567","16digitNo1234567",
"16digitNo1234567","16digitNo1234567","16digitNo1234567"]

def JsonFormatToCopy():
   rs = ""

   rs += "{\\n"
   
   for i in range(0, len(GroupID)):
      rs += "\\t \\\"";
      rs += GroupID[i];
      rs += "\\\": {\\n";
      rs += "\\t \\\"Pwd\\\": \\\"";
      rs += key[i];
      rs+="\\\"\\n"; 
      rs+="\\t}\\n";

   rs+= "}";

   return rs;

print(JsonFormatToCopy())

