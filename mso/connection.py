# ######################################################################################################################
#  MSO Copyright (c) 2025 by Charles L Beyor and Beyotek Inc.                                                          #
#  is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.                          #
#  To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/                            #
#                                                                                                                      #
#  Unless required by applicable law or agreed to in writing, software                                                 #
#  distributed under the License is distributed on an "AS IS" BASIS,                                                   #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                            #
#  See the License for the specific language governing permissions and                                                 #
#  limitations under the License.                                                                                      #
#                                                                                                                      #
#  Gitlab: https://github.com/chuckbeyor101/MSO-Mongo-Schema-Object-Library                                            #
# ######################################################################################################################

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError


def connect_to_mongo(uri: str = "mongodb://localhost:27017", database: str = "mydb", timeout: int = 5000):
    """
    Establish a connection to MongoDB and return the database object.
    
    This helper function simplifies database connection setup by handling
    the MongoClient creation internally, eliminating the need to import
    pymongo separately in your application code.
    
    Args:
        uri (str): The MongoDB connection URI. Defaults to "mongodb://localhost:27017"
        database (str): The name of the database to connect to. Defaults to "mydb"
        timeout (int): Server selection timeout in milliseconds. Defaults to 5000 (5 seconds)
    
    Returns:
        pymongo.database.Database: The database object ready for use with get_model()
    
    Raises:
        ConnectionFailure: If the connection to MongoDB fails
        ConfigurationError: If the URI is malformed or invalid
        ServerSelectionTimeoutError: If the server cannot be reached within the timeout period
        ValueError: If the database name is empty or invalid
    
    Example:
        >>> from mso import connect_to_mongo, get_model
        >>> 
        >>> db = connect_to_mongo("mongodb://localhost:27017", "mydb")
        >>> People = get_model(db, "people")
        
        >>> # With custom timeout
        >>> db = connect_to_mongo("mongodb://localhost:27017", "mydb", timeout=10000)
    """
    if not database or not isinstance(database, str):
        raise ValueError("Database name must be a non-empty string")
    
    if not uri or not isinstance(uri, str):
        raise ValueError("MongoDB URI must be a non-empty string")
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=timeout)
        # Test the connection
        client.admin.command('ping')
        return client[database]
    except ConfigurationError as e:
        raise ConfigurationError(f"Invalid MongoDB URI: {uri}. Error: {str(e)}")
    except ServerSelectionTimeoutError as e:
        raise ServerSelectionTimeoutError(
            f"Could not connect to MongoDB at {uri} within {timeout}ms. "
            f"Please check if MongoDB is running and the URI is correct. Error: {str(e)}"
        )
    except ConnectionFailure as e:
        raise ConnectionFailure(f"Failed to connect to MongoDB at {uri}. Error: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error connecting to MongoDB: {str(e)}")
