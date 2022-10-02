use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use cw_storage_plus::{ Map};


#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct State {
   
}


pub const STATE: Map<(&str, &str), State> = Map::new("state");
