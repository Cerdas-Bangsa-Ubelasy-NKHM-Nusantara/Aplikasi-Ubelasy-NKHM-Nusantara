import React from 'react';

export const groupNotesByMonthYear = (notes) => {
  const groups = {};
  notes.forEach((note) => {
    const date = new Date(note.createdAt);
    const month = date.toLocaleString('id-ID', { month: 'long' });
    const year = date.getFullYear();
    const key = `${month} ${year}`;
    if (!groups[key]) groups[key] = [];
    groups[key].push(note);
  });
  const sortedKeys = Object.keys(groups).sort((a, b) => {
    const dateA = new Date(a);
    const dateB = new Date(b);
    return dateB - dateA;
  });
  const sortedGroups = {};
  sortedKeys.forEach((key) => { sortedGroups[key] = groups[key]; });
  return sortedGroups;
};

export const highlightText = (text, keyword) => {
  if (!keyword || keyword.trim() === '') return text;
  const regex = new RegExp(`(${keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  const parts = text.split(regex);
  return parts.map((part, i) =>
    regex.test(part) ? React.createElement('mark', { key: i }, part) : part
  );
};
