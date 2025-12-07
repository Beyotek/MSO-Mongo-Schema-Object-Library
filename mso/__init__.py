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

"""
MSO - Mongo Schema Object Library

A lightweight Object-Document Mapper (ODM) for MongoDB that generates Python classes
from MongoDB $jsonSchema validators, enabling intuitive Pythonic access to MongoDB documents.

Basic Usage:
    >>> from mso import connect_to_mongo, get_model
    >>> 
    >>> # Connect to MongoDB
    >>> db = connect_to_mongo("mongodb://localhost:27017", "mydb")
    >>> 
    >>> # Get a model (requires collection with $jsonSchema validator)
    >>> People = get_model(db, "people")
    >>> 
    >>> # Create and save a document
    >>> person = People(name="Alice", age=30)
    >>> person.save()
    >>> 
    >>> # Query documents
    >>> alice = People.find_one({"name": "Alice"})
    >>> print(f"{alice.name} is {alice.age} years old")
    >>> 
    >>> # Update and save
    >>> alice.age = 31
    >>> alice.save()

For more examples and documentation, see:
- AI_CODING_GUIDE.md for detailed AI assistant instructions
- .ai/quick-reference.md for quick reference
- README.md for comprehensive documentation
"""

from mso.connection import connect_to_mongo
from mso.generator import get_model

__version__ = "1.0.81"
__all__ = ['connect_to_mongo', 'get_model']
