/*
 * Copyright 2008-present MongoDB, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Original Work: Apache License, Version 2.0, Copyright 2017 Hans-Peter Grahsl.
 */

package com.mongodb.kafka.connect.sink.processor.id.strategy;

import org.apache.kafka.connect.sink.SinkRecord;

import org.bson.BsonDocument;
import org.bson.BsonValue;

import com.mongodb.kafka.connect.sink.converter.SinkDocument;
import com.mongodb.kafka.connect.sink.processor.field.projection.FieldProjector;

public class PartialValueStrategy implements IdStrategy {
    private FieldProjector fieldProjector;

    public PartialValueStrategy(final FieldProjector fieldProjector) {
        this.fieldProjector = fieldProjector;
    }

    @Override
    public BsonValue generateId(final SinkDocument doc, final SinkRecord orig) {
        //NOTE: this has to operate on a clone because
        //otherwise it would interfere with further projections
        //happening later in the chain e.g. for value fields
        SinkDocument clone = doc.clone();
        fieldProjector.process(clone, orig);
        //NOTE: If there is no key doc present the strategy
        //simply returns an empty BSON document per default.
        return clone.getValueDoc().orElseGet(BsonDocument::new);
    }

    public FieldProjector getFieldProjector() {
        return fieldProjector;
    }

}
