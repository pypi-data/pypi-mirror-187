// Copyright (C) 2021 Bosutech XXI S.L.
//
// nucliadb is offered under the AGPL v3.0 and as commercial software.
// For commercial licensing, contact us at info@nuclia.com.
//
// AGPL:
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.
//
use std::path::PathBuf;

use nucliadb_protos::*;

use crate::service_interface::*;

#[derive(Debug)]
pub struct FieldError {
    pub msg: String,
}

impl std::fmt::Display for FieldError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", &self.msg)
    }
}

impl InternalError for FieldError {}

pub struct FieldConfig {
    pub path: PathBuf,
}

pub struct DocumentIterator(Box<dyn Iterator<Item = DocumentItem> + Send>);
impl DocumentIterator {
    pub fn new<I>(inner: I) -> DocumentIterator
    where I: Iterator<Item = DocumentItem> + Send + 'static {
        DocumentIterator(Box::new(inner))
    }
}
impl Iterator for DocumentIterator {
    type Item = DocumentItem;
    fn next(&mut self) -> Option<Self::Item> {
        self.0.next()
    }
}

pub trait FieldReader:
    ReaderChild<Request = DocumentSearchRequest, Response = DocumentSearchResponse>
{
    fn iterator(&self, request: &StreamRequest) -> InternalResult<DocumentIterator>;
    fn count(&self) -> InternalResult<usize>;
}

pub trait FieldWriter: WriterChild {}
