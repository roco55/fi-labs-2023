import { PIGGY_ALPHABET } from "./constants";
import { CipherService } from "./services";
import {VARIANT_FILE, FILE} from './constants'

//USE CIPHER SERVICE INSTANCE FOR ALL OPERATIONS
//IN FILE_CONSTANTS.ts FILE YOU CAN FIND ALL FILE PATHES 

const cipherService = new CipherService(PIGGY_ALPHABET, VARIANT_FILE);


